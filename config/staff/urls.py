from django.urls import path
from .views import LoginView, LogoutView, StaffView , RegisterView, add_category , add_product , checkout , manager , edit_category, OrderFilterView, staff_access,ProductUpdateView, Add_product   

urlpatterns = [
    # URL pattern for the login view
    path("login/", LoginView.as_view(), name="login"),
    # URL pattern for the logout view
    path("logout/", LogoutView.as_view(), name="logout"),
    # URL pattern for viewing the staff list
    path("staff/", StaffView.as_view(), name="staff"),
    # URL pattern for the registration view
    path("register/", RegisterView.as_view(), name="register"),
    path("filter/", OrderFilterView.as_view(), name="filter"),
    # URL pattern for the home view
    # path("filter/", OrderFilterView.as_view(), name="filter"),
    path("add-category/", add_category, name="add-category"),
    path("Add-product.html/", Add_product.as_view(), name="add-product"),
    path("checkout/", checkout, name="checkout"),
    path("Edit-product.html",ProductUpdateView.as_view(), name="edit-product"),
    path("manager/", manager, name="manager"),
    # path("", staff, name="staff"),
    path("edit-category/", edit_category, name="edit-category"),
    path("staff-access/", staff_access, name="staff-access"),
]
