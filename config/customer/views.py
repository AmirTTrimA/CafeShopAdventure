# customers/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from order.models import Order
from .models import Customer


def customer_checkout(request):
    """
    Renders the customer order status page.

    
    Context:
        orders (list): A list of Order objects associated with the 
                       customer's phone number.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response of the 
                      customer order status page.
    """
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

@user_passes_test(lambda u: u.is_staff)
def search_customer(request):
    """
    Searches for customers based on their phone number.

    Context:
        customers (list): A list of Customer objects that match
                          the searched phone number.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response of the customer 
                      search results page.
    """
    customers = []
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number', '')
        if phone_number:
            customers = Customer.objects.filter(phone_number=phone_number)  # جستجوی مشتریان بر اساس شماره تلفن
    return render(request, 'customers/search_customer.html', {'customers': customers})

