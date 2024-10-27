from django.urls import path
from .views import search_customer

urlpatterns = [
    path('search/', search_customer, name='search_customer'),
]
