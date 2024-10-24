from django.shortcuts import render, get_object_or_404
from .models import MenuItem,Category
from django.views import View


class CafeMenuView(View):
    template_name = 'menu.html'

    def get(self, request):
        menu_items = MenuItem.objects.filter(is_available=True)  # Only get available items
        cat_items=Category.objects.all()
        context = {
            'cat_item':cat_items,'menu_items': menu_items
        }
        return render(request, self.template_name, context)
    

class ProductDetailView(View):
    template_name = 'product.html'

    def get(self, request, pk):
        product = get_object_or_404(MenuItem, pk=pk)
        context = {'product': product}
        return render(request, self.template_name, context)
