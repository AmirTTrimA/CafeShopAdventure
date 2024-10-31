from django.urls import path
from . import views

urlpatterns = [
    path('customer/checkout/', views.customer_checkout, name='customer_checkout'),
    path('search/', views.search_customer, name='search_customer'),
]
