from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Order, OrderItem, MenuItem
from .utils import get_cart_from_cookies, set_cart_in_cookies


def add_to_cart(request, item_id):
    """Add a menu item to the cart."""
    menu_item = get_object_or_404(MenuItem, id=item_id)

    # Use cookies to manage the cart
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
    response = JsonResponse(
        {
            "message": f"{menu_item.name} has been added to your cart.",
            "cart": cart,
        }
    )
    set_cart_in_cookies(response, cart)
    return response


def cart_view(request):
    """Display the contents of the cart."""
    cart = get_cart_from_cookies(request)
    return render(request, "cart.html", {"cart": cart})


def submit_order(request):
    """Submit an order based on the items in the cart."""
    cart = get_cart_from_cookies(request)

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_view")

    order = Order.objects.create(customer=request.user.customer)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order, item=item.menu_item, quantity=item.quantity
        )

    # Clear the cart in cookies
    response = redirect("order_success")
    response.delete_cookie("cart")
    messages.success(request, "Your order has been submitted successfully!")
    return response
