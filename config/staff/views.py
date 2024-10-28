# staff/views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from customer.models import Customer

@user_passes_test(lambda u: u.is_staff)
def search_customer(request):
    customers = []
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number', '')
        if phone_number:
            customers = Customer.objects.filter(phone_number=phone_number)
    return render(request, 'staff/search_customer.html', {'customers': customers})
