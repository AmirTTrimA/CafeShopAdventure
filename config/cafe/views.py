from django.shortcuts import render
from django.views import View

class MyView(View):
    def get(self, request):
        return render(request, 'index.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

# def my_view(request):
#     return render(request, 'index.html')  