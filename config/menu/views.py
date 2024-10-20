from django.shortcuts import render, get_object_or_404
from .models import MenuItem,Category

def menu(request):
    products = MenuItem.objects.all().values()
    category=Category.objects.all().values()
    return render(request, 'menu\menu.html', {'product':products,'category':category})

def product_detail(request,product_id):
    queryset=MenuItem.objects.filter(id=product_id)
    product = get_object_or_404(queryset)
    context = {
        'product': product
    }
    return render(request, 'menu\product.html', context)
