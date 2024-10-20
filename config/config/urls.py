from django.contrib import admin
from django.urls import path, include
from menu import views as views_menu
urlpatterns = [
    path("admin/", admin.site.urls),
    path("staff/", include('staff.urls')),
    # path("order/",views_menu.product_detail, name='product.html' ),
    path("menu/",views_menu.menu, name='product' ),
    # path("menu/product.html",views_menu.product_detail, name='product' ),
    path('menu/product/<int:product_id>', views_menu.product_detail, name='product')
]
