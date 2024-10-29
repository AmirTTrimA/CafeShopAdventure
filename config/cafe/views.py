from django.shortcuts import render
from django.views import View
from menu.models import MenuItem, Category

class MyView(View):
    template_name = 'index.html'

    def get(self, request):
        menu_items = MenuItem.objects.filter(is_available=True)  # Only get available items
        cat_items=Category.objects.all()
        context = {
            'cat_item':cat_items,'menu_items': menu_items
        }
        return render(request, self.template_name, context)

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

# def my_view(request):
#     return render(request, 'index.html')  