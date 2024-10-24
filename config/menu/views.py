from django.shortcuts import render, get_object_or_404
from .models import MenuItem,Category
from django.views import View


class CafeMenuView(View):
    template_name = 'menu\menu.html'

    def get(self, request):
        menu_items = MenuItem.objects.filter(is_available=True)
        context = {
            'menu_items': menu_items
        }
        return render(request, self.template_name, context)
    

class ProductDetailView(View):
    template_name = 'menu\product.html'

    def get(self, request, pk):
        product = get_object_or_404(MenuItem, pk=pk)
        context = {'product': product}
        return render(request, self.template_name, context)

def menu_view(request):
    return render(request, 'menu.html') 

def product_view(request):
    return render(request, 'product.html')

def search_view(request):
    return render(request, 'search.html')
