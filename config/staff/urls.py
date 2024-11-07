from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("staff/", views.StaffView.as_view(), name="staff"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("manager/", views.ViewManager.as_view(), name="manager"),
    path("add-category/", views.AddCategory.as_view(), name="add-category"),
    path("Add-product.html/", views.Add_product.as_view(), name="add-product"),
    path("remove-category/", views.RemoveCategory.as_view(), name="remove-c"),
    path("remove-product/", views.RemoveProduct.as_view(), name="remove-p"),
    path("staff-access/", views.StaffAccess.as_view(), name="staff-access"),
    path("Edit-product.html", views.EditProduct.as_view(), name="edit-product"),
    path("checkout/", views.staff_checkout, name="staff_checkout"),
    path("manager_checkout/", views.manager_checkout, name="manager_checkout"),
    path("update_staff/<int:order_id>/", views.update_order_staff, name="update_staff"),
    path("data_analysis.html", views.DataAnalysis.as_view(), name="data_analysis"),
    path("order_details/<int:order_id>/", views.order_details, name="order_details"),
    path("sale_analysis.html", views.SalesAnalysis.as_view(), name="sale_analysis"),
    path(
        "update_order/<int:order_id>/",
        views.update_order_status,
        name="update_order_status",
    ),
    path(
        "staff/order/item/<int:order_id>/add_item/",
        views.add_order_item,
        name="add_order_item",
    ),
    path(
        "staff/order/item/<int:item_id>/update/",
        views.update_order_item,
        name="update_order_item",
    ),
    path(
        "staff/order/item/<int:item_id>/remove/",
        views.remove_order_item,
        name="remove_order_item",
    ),
    path("search_customer/", views.search_customer, name="search_customer"),
    path(
        "report/top-selling-items/", views.top_selling_items, name="top_selling_items"
    ),
    path(
        "report/sales-by-category/", views.sales_by_category, name="sales_by_category"
    ),
    path(
        "report/sales-by-customer/", views.sales_by_customer, name="sales_by_customer"
    ),
    path(
        "report/sales-by-time-of-day/",
        views.sales_by_time_of_day,
        name="sales_by_time_of_day",
    ),
    path(
        "report/order-status-report/",
        views.order_status_report,
        name="order_status_report",
    ),
    path(
        "report/sales-by-employee/",
        views.sales_by_employee_report,
        name="sales_by_employee_report",
    ),
    path(
        "report/customer-order-history/",
        views.customer_order_history_report,
        name="customer_order_history_report",
    ),
    path("export_orders/", views.download_orders, name="export_orders"),
    path("export_customers/", views.download_customers, name="export_customers"),
    path("export_staff/", views.download_staff, name="export_staff"),
    path("export_menu_items/", views.download_menu_items, name="export_menu_items"),
]
