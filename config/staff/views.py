"""views.py"""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse_lazy
from order.models import Order
from customer.models import Customer
from .forms import OrderFilterForm
from .forms import StaffRegistrationForm
from order.models import Order
from customer.models import Customer
from .models import Staff
from .forms import StaffRegistrationForm, OrderFilterForm


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
    """View for staff login."""

    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        user = authenticate(
            request,
            phone_number=phone_number,
            password=password,
            backend="staff.auth.PhoneNumberBackend",
        )

        if user:
            login(request, user)
            if user.is_staff:  # Check if the user is a manager
                return redirect("manager")  # Redirect to manager dashboard
            else:
                return redirect("staff")  # Redirect to staff panel
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
        messages.success(request, "You have been logged out successfully.")
        return redirect("login")


@method_decorator(login_required, name="dispatch")
class ManagerView(View):
    """Render the manager dashboard."""

    template_name = "manager.html"

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class StaffView(View):
    """
    Render the staff page.
    """

    template_name = "staff.html"

    def get(self, request):
        if request.user.is_authenticated:
            """render the staff page"""
            # context = self.get_context_data()
            return render(request, self.template_name, {"login_logout": "logout"})
        else:
            return render(request, self.template_name, {"login_logout": "login"})

    def get_context_data(self, **kwargs):
        context = {}
        return context


class OrderFilterView(View):
    template_name = "staff\order_list.html"

    def get(self, request):
        form = OrderFilterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            filter_type = form.cleaned_data["filter_type"]
            filter_value = form.cleaned_data["filter_value"]
            if filter_type != "last_order" and filter_value == "":
                form.add_error("filter_value", "Please enter a valid value.")

            elif filter_type == "last_order":
                orders = View.Order.objects.order_by("-order_date")[:1]  # Last order
                return render(
                    request, self.template_name, {"form": form, "orders": orders}
                )

            elif filter_type != "last_order" and filter_value != "":
                # Apply filtering based on filter type
                if filter_type == "date":
                    import datetime

                    try:
                        date_filter = datetime.datetime.strptime(
                            filter_value, "%Y-%m-%d"
                        )
                        orders = Order.objects.filter(order_date__date=date_filter)
                    except ValueError:
                        orders = (
                            Order.objects.none()
                        )  # Return no results on invalid date
                elif filter_type == "status":
                    orders = Order.objects.filter(status=filter_value)
                elif filter_type == "table_number":
                    customers = Customer.objects.filter(table_number=filter_value)
                    orders = Order.objects.filter(customer__in=customers)

                return render(
                    request, self.template_name, {"form": form, "orders": orders}
                )

            return render(request, self.template_name, {"form": form})


# def manager(request):
#     return render(request, "manager.html")


class ProductUpdateView(View):

    def get(self, request):
         items=MenuItem.objects.all()
         cats=Category.objects.all()
         return render(request,'Edit-product.html',{'massage':'','items':items,'cats':cats})
    
    def post(self, request):
         name_i = request.get('Prodcut Name')
         item=MenuItem.objects.get(name=name_i)
         items=MenuItem.objects.all()
         cats=Category.objects.all()
         if item:
            item.description =request.Post.get('Product description')
            item.price = request.Post.get('Product Price')
            item.category = request.Post.get('Product cat')
            item.save()
            return render(request,'Edit-product.html',{'items':items,'cats':cats,'massage':'Changes saved successfully'})
         else:
            return render(request,'Edit-product.html',{'items':items,'cats':cats,'massage':'product dose not exist'})

# class EditProductView(View):
#     def get(request):
#         return render(request, "edit-product.html")

class CheckoutView(View):
    def get(request):
        return render(request, "checkout.html")

class AddProductView(View):
    def get(request):
        return render(request, "add-product.html")

class AddCategoryView(View):
    def get(request):
        return render(request, "add-category.html")

class EditCategoryView(View):
    def get(request):
        return render(request, "edit-category.html")



class StaffAccessView(View):
    def get(self, request):
        return render(request, 'staff-access.html')


# class OrderFilterView(View):
#     template_name = 'order_list.html'

#     def get(self, request):
#         form = OrderFilterForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = OrderFilterForm(request.POST)
#         if form.is_valid():
#             filter_type = form.cleaned_data['filter_type']
#             filter_value= form.cleaned_data['filter_value']
#             if filter_type!='last_order' and filter_value =='':
#                 form.add_error('filter_value', 'Please enter a valid value.')

#             elif filter_type == 'last_order' :
#                 orders = Order.objects.order_by('-order_date')[:1]  # Last order
#                 return render(request, self.template_name, {'form': form, 'orders': orders})

#             elif filter_type !='last_order' and filter_value!='':

#             # Apply filtering based on filter type
#                 if filter_type == 'date':
#                     import datetime
#                     try:
#                         date_filter = datetime.datetime.strptime(filter_value, '%Y-%m-%d')
#                         orders = Order.objects.filter(order_date__date=date_filter)
#                     except ValueError:
#                         orders = Order.objects.none()  # Return no results on invalid date
#                 elif filter_type == 'status':
#                     orders = Order.objects.filter(status=filter_value)
#                 elif filter_type == 'table_number':
#                     customers = Customer.objects.filter(table_number=filter_value)
#                     orders = Order.objects.filter(customer__in=customers)

#                 return render(request, self.template_name, {'form': form, 'orders': orders})

#             return render(request, self.template_name, {'form': form})
