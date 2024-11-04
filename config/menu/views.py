from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category
from django.views import View


# class ProductDetailView(View):
#     def get(self, request):
#         return render(request, 'Product.html')
class CafeMenuView(View):
    """
    View to display the cafe's menu.

    If a category_id is provided, only the menu items belonging to that category will be shown.
    Otherwise, all available menu items will be displayed.
    """
    def get(self, request, category_id=None):
        """
        Handles GET requests to fetch and display menu items.
        """
        if category_id:
            menu_items = MenuItem.objects.filter(category_id=category_id)
        else:
            menu_items = MenuItem.objects.all()

        cat_item = Category.objects.all()
        return render(
            request, "menu.html", {"menu_items": menu_items, "cat_item": cat_item}
        )


# class CafeMenuView(View):
#     template_name = "menu.html"

#     def get(self, request):
#         menu_items = MenuItem.objects.filter(
#             is_available=True
#         )  # Only get available items
#         cat_items = Category.objects.all()
#         context = {"cat_item": cat_items, "menu_items": menu_items}
#         return render(request, self.template_name, context)


class ProductDetailView(View):
    """
    View to display the details of a specific product (menu item).
    """
    template_name = "product.html"

    def get(self, request, pk):
        """
        Handles GET requests to fetch and display the details
        """
        product = get_object_or_404(MenuItem, pk=pk)
        context = {"product": product}
        return render(request, self.template_name, context)


# class SearchView(View):
#     def get(self, request):
#         return render(request, "search.html")


class SearchView(View):
    """
    View to handle searching for menu items based on a query string.

    This view retrieves menu items whose names contain the search query.
    """
    def get(self, request):
        """
        Handles GET requests to search for menu items based on the query.
        """
        query = request.GET.get("q")
        if query:
            menu_items = MenuItem.objects.filter(name__icontains=query)
        else:
            menu_items = MenuItem.objects.none()
        return render(request, "search.html", {"menu_items": menu_items})
