from django.urls import path
from . import views

urlpatterns = [
    path("add_to_cart/<int:item_id>/", views.add_to_cart_view, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path(
        "remove_from_cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("submit_order/", views.submit_order, name="submit_order"),
    path("order_success/", views.order_success, name="order_success"),
    path(
        "order/manage/<int:order_id>/",
        views.manage_order_items,
        name="manage_order_items",
    ),
    path(
        "order/change_status/<int:order_id>/",
        views.change_order_status,
        name="change_order_status",
    ),
    path(
        "order/confirmation/<int:order_id>/",
        views.order_confirmation,
        name="order_confirmation",
    ),
    path("order_history/", views.order_history_view, name="order_history_view"),
]
