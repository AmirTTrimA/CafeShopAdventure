from django.urls import path
from .views import LoginView, LogoutView, StaffView, RegisterView

urlpatterns = [
    # URL pattern for the login view
    path("login/", LoginView.as_view(), name="login"),
    # URL pattern for the logout view
    path("logout/", LogoutView.as_view(), name="logout"),
    # URL pattern for viewing the staff list
    path("", StaffView.as_view(), name="staff"),
    # URL pattern for the registration view
    path("register/", RegisterView.as_view(), name="register"),
    path('orders/', views_staff.order_list, name='order_list'),
]
