from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem, Cart, CartItem, MenuItem


@login_required
def add_to_cart(request, item_id):
    """Add a menu item to the customer's cart."""
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{menu_item.name} has been added to your cart.")
    return redirect("cart_view")


@login_required
def cart_view(request):
    """Display the contents of the customer's cart."""
    cart = get_object_or_404(Cart, customer=request.user.customer)
    return render(request, "cart.html", {"cart": cart})


@login_required
def submit_order(request):
    """Submit an order based on the items in the customer's cart."""
    cart = get_object_or_404(Cart, customer=request.user.customer)

    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_view")

    order = Order.objects.create(customer=request.user.customer)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order, item=item.menu_item, quantity=item.quantity
        )

    cart.items.all().delete()

    messages.success(request, "Your order has been submitted successfully!")
    return redirect("order_success")
