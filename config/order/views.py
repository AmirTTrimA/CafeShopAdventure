"""order/views.py

This module defines views for managing orders, including adding items to the cart,
submitting orders, and viewing order history.
"""

import uuid
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from .forms import OrderForm
from .models import Order, OrderItem, OrderHistory, MenuItem, Customer
from .utils import get_cart_from_cookies, set_cart_in_cookies

DEFAULT_GUEST_CUSTOMER_PHONE = "09123456789"  # Default phone number for guest customer


def add_to_cart(request, item_id):
    """Add a menu item to the cart.

    Args:
        request: The HTTP request object.
        item_id (int): The ID of the menu item to add to the cart.

    Returns:
        JsonResponse: A response containing a message and the updated cart.
    """
    menu_item = get_object_or_404(MenuItem, id=item_id)

    # Get cart from cookies
    cart = get_cart_from_cookies(request)

    # Add item to cart
    if str(menu_item.id) in cart:
        cart[str(menu_item.id)]["quantity"] += 1
    else:
        cart[str(menu_item.id)] = {
            "name": menu_item.name,
            "price": str(menu_item.price),
            "quantity": 1,
        }

    # Save updated cart in cookies
    set_cart_in_cookies(request, cart)

    return JsonResponse(
        {
            "message": f"{menu_item.name} has been added to your cart.",
            "cart": cart,
        }
    )


def cart_view(request):
    """Display the contents of the cart.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered cart view.
    """
    cart = get_cart_from_cookies(request)
    return render(request, "cart.html", {"cart": cart})


def submit_order(request):
    """Submit an order based on the items in the cart.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to order success page or renders the order form.
    """
    cart = get_cart_from_cookies(request)

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")

            if phone_number:
                customer, created = Customer.objects.get_or_create(
                    phone_number=phone_number
                )
            else:
                guest_id = str(uuid.uuid4())
                customer = None  # No customer linked

            # Create the order
            order = Order.objects.create(customer=customer)

            # Iterate through cart items and create OrderItems
            for item_id, item_data in cart.items():
                menu_item = MenuItem.objects.get(id=item_id)  # Fetch the menu item
                OrderItem.objects.create(
                    order=order, item=menu_item, quantity=item_data["quantity"]
                )

            # Store order history
            if customer:
                OrderHistory.objects.create(customer=customer, order_data=cart)
            else:
                OrderHistory.objects.create(guest_id=guest_id, order_data=cart)

            set_cart_in_cookies(request, {})
            messages.success(request, "Your order has been submitted successfully!")
            return redirect("order_success")
    else:
        form = OrderForm()

    return render(request, "submit_order.html", {"form": form, "cart": cart})


# مدیریت آیتم‌های سفارش توسط کاربران Staff
@login_required
def manage_order_items(request, order_id):
    """Allow staff to add or remove items from an order."""
    order = get_object_or_404(Order, id=order_id)

    # اطمینان از اینکه کاربر یک عضو staff است
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to manage this order.")
        return redirect("order_list")

    if request.method == "POST":
        if "add_item" in request.POST:
            item_id = request.POST.get("item_id")
            quantity = int(request.POST.get("quantity", 1))

            menu_item = get_object_or_404(MenuItem, id=item_id)
            OrderItem.objects.create(
                order=order, menu_item=menu_item, quantity=quantity
            )

            messages.success(request, f"{menu_item.name} has been added to the order.")

        elif "remove_item" in request.POST:
            item_id = request.POST.get("item_id")
            order_item = get_object_or_404(OrderItem, id=item_id, order=order)
            order_item.delete()

            messages.success(
                request, f"{order_item.menu_item.name} has been removed from the order."
            )

        return redirect("manage_order_items", order_id=order.id)

    order_items = order.cart_items.all()
    return render(
        request, "manage_order_items.html", {"order": order, "order_items": order_items}
    )


# تغییر وضعیت سفارش
@login_required
def change_order_status(request, order_id):
    """Allow staff to change the status of an order."""
    order = get_object_or_404(Order, id=order_id)

    # اطمینان از اینکه کاربر یک عضو staff است
    if not request.user.is_staff:
        messages.error(
            request, "You do not have permission to change the status of this order."
        )
        return redirect("order_list")

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(
                request,
                f"The status of Order {order.id} has been changed to {new_status}.",
            )
        else:
            messages.error(request, "Invalid status selected.")

        return redirect("order_list")

    return render(request, "change_order_status.html", {"order": order})


# فرآیند Checkout (پرداخت)
@login_required
def checkout(request):
    """Handle the checkout process, calculating the total price and creating an order."""
    customer_cart = get_object_or_404(Cart, customer=request.user.customer)

    if customer_cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_view")

    total_price = customer_cart.get_total_price()

    if request.method == "POST":
        order = Order.objects.create(customer=request.user.customer)
        for item in customer_cart.items.all():
            order.cart_items.add(item)

        order.calculate_total_price()
        order.status = "Pending"
        order.save()

        customer_cart.items.all().delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect("order_confirmation", order_id=order.id)

    return render(
        request, "checkout.html", {"cart": customer_cart, "total_price": total_price}
    )


# تأیید سفارش
@login_required
def order_confirmation(request, order_id):
    """Show the order confirmation after checkout."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_confirmation.html", {"order": order})


def order_status_cleanup(request):
    """Clean up old orders that are 'Canceled' or 'Completed'."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to clean up orders.")
        return redirect("order_list")

    # تعیین محدوده زمانی برای سفارش‌های قدیمی. مثلا سفارش‌هایی که بیش از 30 روز پیش ایجاد شده‌اند
    time_threshold = timezone.now() - timedelta(days=30)

    # پیدا کردن سفارش‌هایی که وضعیت آنها 'Canceled' یا 'Completed' است و بیش از 30 روز پیش ایجاد شده‌اند
    old_orders = Order.objects.filter(
        status__in=["Canceled", "Completed"], created_at__lt=time_threshold
    )

    # حذف این سفارش‌ها
    deleted_count, _ = old_orders.delete()

    # نمایش پیغام به کاربر درباره تعداد سفارش‌های حذف شده
    messages.success(request, f"{deleted_count} old orders have been cleaned up.")

    return redirect("order_list")


@login_required
def change_item_quantity(request, order_id, item_id):
    """Allow staff to change the quantity of an item in an order."""

    # پیدا کردن سفارش و آیتم مربوطه
    order = get_object_or_404(Order, id=order_id)
    order_item = get_object_or_404(OrderItem, order=order, menu_item_id=item_id)

    # بررسی اینکه آیا کاربر یک عضو staff است
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to change item quantities in this order.",
        )
        return redirect("order_list")

    if request.method == "POST":
        # دریافت مقدار جدید از فرم
        new_quantity = int(request.POST.get("quantity", 1))

        # بررسی اینکه مقدار جدید معتبر است
        if new_quantity > 0:
            order_item.quantity = new_quantity
            order_item.save()  # ذخیره آیتم با مقدار جدید
            messages.success(
                request,
                f"The quantity of {order_item.menu_item.name} has been updated to {new_quantity}.",
            )
        else:
            messages.error(request, "Quantity must be greater than zero.")

        # محاسبه مجدد قیمت کل سفارش
        order.calculate_total_price()
        order.save()  # ذخیره سفارش با قیمت جدید

        return redirect("manage_order_items", order_id=order.id)

    return render(
        request, "change_item_quantity.html", {"order": order, "order_item": order_item}
    )



def order_history_view(request):
    """Display the customer's order history.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered order history view or redirects to login.
    """
    phone_number = request.GET.get(
        "phone_number"
    )  # Optional: Get phone number to filter

    if phone_number:
        customer = get_object_or_404(Customer, phone_number=phone_number)
        orders = OrderHistory.objects.filter(customer=customer).order_by("-created_at")
        return render(request, "order_history.html", {"orders": orders})
    else:
        guest_id = request.session.get("guest_id")
        if guest_id:
            orders = OrderHistory.objects.filter(guest_id=guest_id).order_by(
                "-created_at"
            )
            return render(request, "order_history.html", {"orders": orders})
        else:
            messages.warning(
                request,
                "You need to provide a phone number or be logged in to view your order history.",
            )
            return redirect("login")