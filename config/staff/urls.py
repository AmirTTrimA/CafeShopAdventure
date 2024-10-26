from django.urls import path
from .views import (LoginView, LogoutView, StaffView ,
                     RegisterView, add_category , add_product , checkout , manager ,
                       edit_category, OrderFilterView, staff_access,EditProduct,
                         Add_product,AddCategory,RemoveProduct,RemoveCategory)   

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
    path("add-category/",  AddCategory.as_view(), name="add-category"),
    path("Add-product.html/", Add_product.as_view(), name="add-product"),
    path('remove-category/', RemoveCategory.as_view(), name='remove-c'),
    path('remove-product/', RemoveProduct.as_view(), name='remove-p'),
    path("Edit-product.html",EditProduct.as_view(), name="edit-product"),
    path("manager/", manager, name="manager"),
    # path("", staff, name="staff"),
    path("edit-category/", edit_category, name="edit-category"),
    path("staff-access/", staff_access, name="staff-access"),
]
