from django.urls import path
from .views import customer_checkout, search_customer

urlpatterns = [
    path('customer/checkout/', customer_checkout, name='customer_checkout'),
    path('search/', search_customer, name='search_customer'),
]
