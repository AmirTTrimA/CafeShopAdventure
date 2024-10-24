"""views.py"""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse_lazy

from .models import Staff
from .forms import StaffRegistrationForm


# class RegisterView(FormView):
#     template_name = "staff/register.html"
#     form_class = StaffRegistrationForm
#     success_url = reverse_lazy("login")

#     def form_valid(self, form):
#         form.save()
#         messages.success(self.request, "Staff registered successfully!")
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.error(self.request, "There was an error in the registration form.")
#         return super().form_invalid(form)


# class LoginView(View):
#     template_name = "staff/login.html"

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         phone_number = request.POST.get("phone_number")
#         password = request.POST.get("password")
#         user = authenticate(request, phone_number=phone_number, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("staff")
#         else:
#             messages.error(request, "Invalid phone number or password.")
#             return render(request, self.template_name)


# @method_decorator(login_required, name="dispatch")
# class LogoutView(View):
#     """
#     Handle staff logout.

#     Logs out the user and redirects to the login page.
#     """

#     def get(self, request):
#         logout(request)
#         return redirect("login")


# @method_decorator(login_required, name="dispatch")
# class StaffView(View):
#     """
#     Render the staff page.
#     """

#     template_name = "staff.html"

#     def get(self, request):
#         context = self.get_context_data()
#         return render(request, self.template_name, context)

#     def get_context_data(self, **kwargs):
#         context = {}
#         return context

class RegisterView(FormView):
    template_name = "login.html"
    form_class = StaffRegistrationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Staff registered successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in the registration form.")
        return super().form_invalid(form)


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)
            return redirect("staff")
        else:
            messages.error(request, "Invalid phone number or password.")
            return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    """
    Handle staff logout.

    Logs out the user and redirects to the login page.
    """

    def get(self, request):
        logout(request)
        return redirect("login")


@method_decorator(login_required, name="dispatch")
class StaffView(View):
    """
    Render the staff page.
    """

    template_name = "staff.html"

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {}
        return context
    

def manager(request):
    return render(request, 'manager.html')
  
def edit_product(request):
    return render(request, 'edit-product.html')
  
def checkout(request):
    return render(request, 'checkout.html')
  
def add_product(request):
    return render(request, 'add-product.html')  
  
def add_category(request):
    return render(request, 'add-category.html')  

def edit_category(request):
    return render(request, 'edit-category.html')  
