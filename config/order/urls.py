# urls.py
from django.urls import path
from .views import add_to_cart, cart_view, submit_order, order_history_view

urlpatterns = [
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('submit_order/', submit_order, name='submit_order'),
    path('order_history/', order_history_view, name='order_history'),
]
