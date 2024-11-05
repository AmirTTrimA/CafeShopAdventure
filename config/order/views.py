"""order/views.py

This module defines views for managing orders, including adding items to the cart,
submitting orders, and viewing order history.
"""

import json
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from cafe.models import Cafe
from staff.models import Staff
from .models import Order, OrderItem, OrderHistory, MenuItem, Customer


DEFAULT_GUEST_CUSTOMER_PHONE = "09123456789"  # Default phone number for guest customer


def add_to_cart(response, request, item_id):
    """Add a menu item to the cart."""
    menu_item = get_object_or_404(MenuItem, id=item_id)

    quantity = int(request.GET.get('quantity'))

    cart = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart)

    if item_id in cart:
        cart[item_id]["quantity"] += quantity
    else:
        cart[item_id] = {
            "name": menu_item.name,
            "quantity": quantity,
            "price": str(menu_item.price),
        }

    response = HttpResponse("Item added to cart")
    response.set_cookie("cart", json.dumps(cart), max_age=3600)

    return response


def add_to_cart_view(request, item_id):
    if request.method == "GET":
        quantity = int(request.GET.get("quantity"))
        print(f"Adding item {item_id} with quantity {quantity} to cart.")
        response = redirect("menu")
        response = add_to_cart(response, request, item_id)
        return response
    return redirect("menu")


def remove_from_cart(request, item_id):
    # Check if the cart exists in the session
    cart = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart)

    # Remove the item if it exists in the cart
    if item_id in cart:
        del cart[item_id]
        response = HttpResponse("Item removed from cart")
        response.set_cookie("cart", json.dumps(cart), max_age=3600)
    else:
        return HttpResponse("Item not found in cart.", status=404)

    return redirect("cart")  # Redirect back to the cart page


def cart_view(request):
    """Display the contents of the cart.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered cart view.
    """
    cart = request.COOKIES.get("cart", "{}")
    cart = json.loads(cart)

    total_price = 0.0
    for item_id, item in cart.items():
        item_total = float(item["price"]) * item["quantity"]
        item["total"] = item_total  # Add item total to each item
        total_price += item_total

    
    context = {
            'cart': cart,
            'total_price': total_price,
        }

    return render(request, "cart.html", context)


def submit_order(request):
    if request.method == "POST":
        # Retrieve form data
        table_number = request.POST.get("table_number")
        phone_number = request.POST.get("phone_number")

        # Ensure table_number is valid
        if not table_number:
            messages.error(request, "Table number is required.")
            return redirect("order_form")  # Redirect to the form page

        # Create or get the customer (unpack the tuple)
        customer, created = Customer.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                "cafe": Cafe.objects.first(),
                "table_number": table_number,
                "points": 0,
            },
        )

        # Create the order instance
        order = Order.objects.create(
            customer=customer,
            table_number=table_number,
            order_date=timezone.now(),
            total_price=0.00,  # Will be calculated later
        )

        request.session["customer_phone_number"] = order.customer.phone_number

        # Add order items based on the cart
        cart = request.COOKIES.get("cart", "{}")
        cart = json.loads(cart)
        for item_id, item in cart.items():
            try:
                menu_item = MenuItem.objects.get(
                    id=item_id
                )  # Get the MenuItem instance
                quantity = item["quantity"]

                # Create OrderItem instance
                order_item = OrderItem.objects.create(
                    order=order, item=menu_item, quantity=quantity
                )
                customer.points += menu_item.points * quantity  # Now this works
                print(customer.points)
            except MenuItem.DoesNotExist:
                messages.error(request, f"Menu item with ID {item_id} does not exist.")
                continue  # Skip this item and move to the next

        customer.save()
        # Calculate the total price for the order
        order.calculate_total_price()
        order.save()

        # Clear the cart after order submission
        clear_cart = ""
        response = HttpResponse("Order submitted")
        response.set_cookie("cart", json.dumps(clear_cart), max_age=0)

        messages.success(request, "Order submitted successfully!")
        return redirect("order_success")
    else:
        return render(request, "cart.html")


def order_success(request):
    """Render the order success page."""
    return render(request, "order_success.html")


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
