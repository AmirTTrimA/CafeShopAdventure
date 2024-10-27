from django.urls import path
from .views import customer_checkout  # Import the view

urlpatterns = [
    path('customer/checkout/', customer_checkout, name='customer_checkout'),  # Add this line
]
