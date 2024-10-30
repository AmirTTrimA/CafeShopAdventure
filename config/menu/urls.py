from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.SearchView.as_view() , name="search"),
    path("menu/", views.CafeMenuView.as_view(), name="menu"),
    path("product/<int:pk>", views.ProductDetailView.as_view(), name="product"),
    # path("product/", ProductDetailView.as_view(), name="product"),
]
