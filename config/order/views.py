from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Cart, CartItem, MenuItem


@login_required
def add_to_cart(request, item_id):
    menu_item = MenuItem.objects.get(id=item_id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_view")


@login_required
def cart_view(request):
    cart = Cart.objects.get(customer=request.user.customer)
    return render(request, "cart.html", {"cart": cart})


@login_required
def submit_order(request):
    cart = Cart.objects.get(customer=request.user.customer)
    order = Order.objects.create(customer=request.user.customer)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order, item=item.menu_item, quantity=item.quantity
        )

    cart.items.all().delete()

    return redirect("order_success")
