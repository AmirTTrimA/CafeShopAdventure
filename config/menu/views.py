from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import MenuItem, Category


class CafeMenuView(View):
    def get(self, request, category_id=None):
        if category_id:
            menu_items = MenuItem.objects.filter(category_id=category_id)
        else:
            menu_items = MenuItem.objects.all()

        cat_item = Category.objects.all()
        return render(
            request, "menu.html", {"menu_items": menu_items, "cat_item": cat_item}
        )


class ProductDetailView(View):
    template_name = "product.html"

    def get(self, request, pk):
        product = get_object_or_404(MenuItem, pk=pk)
        context = {"product": product}
        return render(request, self.template_name, context)


class SearchView(View):
    def get(self, request):
        query = request.GET.get("q")
        if query:
            menu_items = MenuItem.objects.filter(name__icontains=query)
        else:
            menu_items = MenuItem.objects.none()
        return render(request, "search.html", {"menu_items": menu_items})
