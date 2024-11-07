from django.shortcuts import render
from django.views import View
from menu.models import MenuItem, Category


class MyView(View):
    """
    A view that handles the display of the main menu items on the index page.
    """

    template_name = "index.html"

    def get(self, request):
        """
        Handles GET requests for the index page.
        """
        menu_items = MenuItem.objects.filter(
            is_available=True
        )  # Only get available items
        cat_items = Category.objects.all()
        context = {"cat_item": cat_items, "menu_items": menu_items}
        return render(request, self.template_name, context)


class ContactView(View):
    """
    A view that handles displaying the contact page.

    This view renders the contact.html template for users to see contact information.
    """

    def get(self, request):
        """
        Handles GET requests for the contact page.
        """
        return render(request, "contact.html")


class AboutView(View):
    """
    A view that handles displaying the about page.

    This view renders the about.html template to provide information about the
    application or organization.
    """

    def get(self, request):
        return render(request, "about.html")
