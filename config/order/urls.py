from django.urls import path
from .views import (
    add_to_cart,
    cart_view,
    submit_order,
    manage_order_items,
    change_order_status,
    checkout,
    order_confirmation,
)

urlpatterns = [
    path("add_to_cart/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_view, name="cart"),
    path("submit_order/", submit_order, name="submit_order"),
    # path('order_history/', order_history_view, name='order_history'),
    path("order/manage/<int:order_id>/", manage_order_items, name="manage_order_items"),
    path(
        "order/change_status/<int:order_id>/",
        change_order_status,
        name="change_order_status",
    ),
    path("checkout/", checkout, name="checkout"),
    path(
        "order/confirmation/<int:order_id>/",
        order_confirmation,
        name="order_confirmation",
    ),
]
