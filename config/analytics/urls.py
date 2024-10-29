from django.urls import path
from .views import CustomerAnalyticsView, OrdersView
urlpatterns = [
    path('customer-analytics/', CustomerAnalyticsView.as_view() , name='customer-analytics'),
    path('orders/', OrdersView.as_view() , name='orders'),

]
