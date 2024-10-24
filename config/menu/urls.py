from django.urls import path
from .views import menu_view, product_view, search_view

urlpatterns = [
    path('menu/', menu_view, name='menu_view'),
    path('product/', product_view, name='product_view'),
    path('search/', search_view, name='search_view'),
]
