from django.urls import path
from .views import LoginView, LogoutView, StaffView , RegisterView, AddCategoryView , AddProductView , CheckoutView , EditProductView, ManagerView , EditCategoryView, OrderFilterView, StaffAccessView, ManagerView

urlpatterns = [
    # URL pattern for the login view
    path("login/", LoginView.as_view(), name="login"),
    # URL pattern for the logout view
    path("logout/", LogoutView.as_view(), name="logout"),
    # URL pattern for viewing the staff list
    path("staff/", StaffView.as_view(), name="staff"),
    # URL pattern for the manager view
    path("manager/", ManagerView.as_view(), name="manager"),
    # URL pattern for the registration view
    path("register/", RegisterView.as_view(), name="register"),
    path("filter/", OrderFilterView.as_view(), name="filter"),
    # URL pattern for the home view
    # path("filter/", OrderFilterView.as_view(), name="filter"),
    path("add-category/", AddCategoryView.as_view(), name="add-category"),
    path("add-product/", AddProductView.as_view(), name="add-product"),
    path("checkout/", CheckoutView.as_view() , name="checkout"),
    path("edit-product/", EditProductView.as_view(), name="edit-product"),
    # path("manager/", manager, name="manager"),
    # path("", staff, name="staff"),
    path("edit-category/", EditCategoryView.as_view(), name="edit-category"),
    path("staff-access/", StaffAccessView.as_view(), name="staff-access"),
]