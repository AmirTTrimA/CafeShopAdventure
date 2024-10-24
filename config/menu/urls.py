from django.urls import path
from .views import ProductDetailView, CafeMenuView, menu_view, product_view, search_view

urlpatterns = [path("", CafeMenuView.as_view(), name="menu"),
               path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
               path('menu/', menu_view, name='menu_view'),
               path('product/', product_view, name='product_view'),
               path('search/', search_view, name='search_view'),
]
