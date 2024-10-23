from django.contrib import admin
from django.urls import path, include
# from django.views import search_products, add_to_cart, cart_view, submit_order, manage_order_items, change_order_status
# from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('cafe.urls')),
    # path("staff/", include('staff.urls')),
    # path("order/", include('order.urls')),
    # path('search/', search_products, name='search_products'),  
    # path("add_to_cart/<int:item_id>/", add_to_cart, name="add_to_cart"),
    # path("cart/", cart_view, name="cart_view"),
    # path("submit_order/", submit_order, name="submit_order"),
    # path("order/manage/<int:order_id>/", manage_order_items, name="manage_order_items"),
    # path("order/change_status/<int:order_id>/", change_order_status, name="change_order_status"),
    # path('checkout/', views.checkout, name='checkout'),
    # path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]