from django.urls import path
from .views import login_view, logout_view, staff_view, register_view, home_view

urlpatterns = [
    # URL pattern for the login view
    path("login/", login_view, name="login"),
    # URL pattern for the logout view
    path("logout/", logout_view, name="logout"),
    # URL pattern for viewing the staff list
    path("staff/", staff_view, name="staff"),
    # URL pattern for the registration view
    path("register/", register_view, name="register"),
    # URL pattern for the home view
    path("home/", home_view, name="home"),
]
