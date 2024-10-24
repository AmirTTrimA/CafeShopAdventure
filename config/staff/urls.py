from django.urls import path
from .views import LoginView, LogoutView, StaffView , RegisterView, add_category , add_product , checkout , edit_product, manager , edit_category, home_view, OrderFilterView

urlpatterns = [
    # URL pattern for the login view
    path("login/", LoginView.as_view(), name="login"),
    # URL pattern for the logout view
    path("logout/", LogoutView.as_view(), name="logout"),
    # URL pattern for viewing the staff view
    path("", StaffView.as_view(), name="staff"),
    # URL pattern for the registration view
    path("register/", RegisterView.as_view(), name="register"),
    # URL pattern for the registration view
    path("register/", RegisterView.as_view(), name="register"),
    # URL pattern for the home view
    path("home/", home_view, name="home"),
    path("filter/", OrderFilterView.as_view(), name="filter")
    path("add-category/", add_category, name="add-category"),
    path("add-product/", add_product, name="add-product"),
    path("checkout/", checkout, name="checkout"),
    path("edit-product/", edit_product, name="edit-product"),
    path("manager/", manager, name="manager"),
    path("edit-category/", edit_category, name="edit-category"),
]
