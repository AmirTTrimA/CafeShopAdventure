from django.shortcuts import render

def customer_analytics_view(request):
    return render(request, 'customer-analytics.html')  

def orders_view(request):
    return render(request, 'orders.html')  
