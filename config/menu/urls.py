from django.urls import path
from .views import ProductDetailView,CafeMenuView

urlpatterns = [path("", CafeMenuView.as_view(), name="menu"),
               path('product/<int:pk>', ProductDetailView.as_view(), name='product'),]