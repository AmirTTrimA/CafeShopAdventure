# customers/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Customer

# این دکوراتور بررسی می‌کند که آیا کاربر عضو کادر است یا خیر
@user_passes_test(lambda u: u.is_staff)
def search_customer(request):
    customers = []
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number', '')
        if phone_number:
            customers = Customer.objects.filter(phone_number=phone_number)  # جستجوی مشتریان بر اساس شماره تلفن
    return render(request, 'customers/search_customer.html', {'customers': customers})
