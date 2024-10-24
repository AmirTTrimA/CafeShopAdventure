from django.urls import path
from .views import ProductDetailView, CafeMenuView, search_view

urlpatterns = [
    path("search/", search_view, name="search_view"),
    path("", CafeMenuView.as_view(), name="menu"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product"),
]
