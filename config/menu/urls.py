from django.urls import path
from .views import SearchView, CafeMenuView, ProductDetailView

urlpatterns = [
    path("search/", SearchView.as_view() , name="search"),
    path("menu/", CafeMenuView.as_view(), name="menu"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product"),
    path("menu/<int:category_id>/", CafeMenuView.as_view(), name="menu_by_category"),
]
