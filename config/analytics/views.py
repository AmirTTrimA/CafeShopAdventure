from django.shortcuts import render
from django.views import View

class CustomerAnalyticsView(View):
    def get(self, request):
        return render(request, 'customer-analytics.html')

class OrdersView(View):
    def get(self, request):
        return render(request, 'orders.html')

