from django.urls import path
from .views import add_to_cart, cart_view, submit_order, manage_order_items, change_order_status

urlpatterns = [
    path("add_to_cart/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_view, name="cart_view"),
    path("submit_order/", submit_order, name="submit_order"),
    path("order/manage/<int:order_id>/", manage_order_items, name="manage_order_items"),
    path("order/change_status/<int:order_id>/", change_order_status, name="change_order_status"),
]
