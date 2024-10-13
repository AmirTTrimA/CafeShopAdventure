"""
urls.py

This module defines the URL patterns for the staff application,
mapping URLs to their corresponding views.
"""

from django.urls import path
from .views import register, login_view, home

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
]
