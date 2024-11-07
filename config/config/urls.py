from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('cafe.urls')),
    path('', include('menu.urls')),
    path('', include('order.urls')),
    # path('', include('analytics.urls')),
    path('', include('customer.urls')),
    path('', include('staff.urls')),
    # path("", include("staff.urls")),
    # path("search_customer/", include("staff.urls")),
]
