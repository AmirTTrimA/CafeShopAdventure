from django.urls import path
from . import views
urlpatterns = [
    path('customer-analytics/', views.CustomerAnalyticsView.as_view() , name='customer-analytics'),
    path('orders/', views.OrdersView.as_view() , name='orders'),

]
