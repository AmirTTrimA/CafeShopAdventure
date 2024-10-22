"""order/views.py

This module defines views for managing orders, including adding items to the cart,
submitting orders, and viewing order history.
"""

import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

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
