from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, CartItem, MenuItem, OrderItem, Cart

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
            order=order, menu_item=item.menu_item, quantity=item.quantity
        )

    cart.items.all().delete()

    messages.success(request, "Your order has been submitted successfully!")
    return redirect("order_success")


@login_required
def manage_order_items(request, order_id):
    """Allow staff to add or remove items from an order."""
    order = get_object_or_404(Order, id=order_id)

    # Ensure that the user is a staff member
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to manage this order.")
        return redirect("order_list")  # Redirect to a list of orders or a suitable page

    if request.method == "POST":
        if 'add_item' in request.POST:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))  # Ensure quantity is an integer

            menu_item = get_object_or_404(MenuItem, id=item_id)
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)

            messages.success(request, f"{menu_item.name} has been added to the order.")
        
        elif 'remove_item' in request.POST:
            item_id = request.POST.get('item_id')
            order_item = get_object_or_404(OrderItem, id=item_id, order=order)
            order_item.delete()

            messages.success(request, f"{order_item.menu_item.name} has been removed from the order.")

        return redirect('manage_order_items', order_id=order.id)  # Redirect to the same page to see updates

    order_items = order.orderitem_set.all()  # Get all items for the order
    return render(request, "manage_order_items.html", {"order": order, "order_items": order_items})

@login_required
def change_order_status(request, order_id):
    """Allow staff to change the status of an order."""
    order = get_object_or_404(Order, id=order_id)

    # Ensure that the user is a staff member
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to change the status of this order.")
        return redirect("order_list")  # Redirect to a list of orders or a suitable page

    if request.method == "POST":
        new_status = request.POST.get('status')  # Get the new status from the form
        if new_status in dict(Order.STATUS_CHOICES).keys():  # Check if the status is valid
            order.status = new_status  # Change the order's status
            order.save()  # Save the changes to the database
            messages.success(request, f"The status of Order {order.id} has been changed to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")

        return redirect('order_list')  # Redirect to the order list after updating status

    return render(request, "change_order_status.html", {"order": order})
