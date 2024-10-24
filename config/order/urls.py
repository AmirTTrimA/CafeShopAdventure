from django.urls import path
from . import views

urlpatterns = [
    path("add_to_cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart_view"),
    path("submit_order/", views.submit_order, name="submit_order"),
    path("order/manage/<int:order_id>/", views.manage_order_items, name="manage_order_items"),
    path("order/change_status/<int:order_id>/", views.change_order_status, name="change_order_status"),
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('cleanup_orders/', views.order_status_cleanup, name='order_status_cleanup'),
    path('order/<int:order_id>/change_quantity/<int:item_id>/', views.change_item_quantity, name='change_item_quantity'),
    path("submit_order/", views.submit_order, name="submit_order"),
]

