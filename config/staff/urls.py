from django.urls import path
from . import views

urlpatterns = [
    path('search-customer/', views.search_customer, name='search_customer'),
]
