from django.urls import path
from .views import customer_analytics_view, orders_view

urlpatterns = [
    path('customer-analytics/', customer_analytics_view, name='customer_analytics_view'),
    path('orders/', orders_view, name='orders_view'),

]
