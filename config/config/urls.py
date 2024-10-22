from django.contrib import admin
from django.urls import path, include
from staff import views as views_staff
urlpatterns = [
    path("admin/", admin.site.urls),
    path("staff/", include('staff.urls')),
    path("menu/", include('menu.urls')),
   
    path('orders/', views_staff.order_list, name='order_list'),
]

