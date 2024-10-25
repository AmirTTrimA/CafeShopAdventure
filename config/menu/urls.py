from django.urls import path
from .views import ProductDetailView, CafeMenuView, SearchView

urlpatterns = [
    path("search/", SearchView.as_view() , name="search"),
    path("menu/", CafeMenuView.as_view(), name="menu"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product"),
    # path("product/", ProductDetailView.as_view(), name="product"),
]
