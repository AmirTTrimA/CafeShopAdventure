from django.shortcuts import render
from order.models import Order  # Import your Order model


def customer_checkout(request):
    # Retrieve the customer's phone number from the session
    customer_phone_number = request.session.get("customer_phone_number")

    # Fetch orders for the customer based on the phone number
    if customer_phone_number:
        orders = Order.objects.filter(
            customer__phone_number=customer_phone_number
        )  # Use double underscore to access related fields
    else:
        orders = []

    return render(request, "customer_order_status.html", {"orders": orders})
