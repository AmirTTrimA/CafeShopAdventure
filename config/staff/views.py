"""staff/views.py"""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse_lazy
from .forms import OrderFilterForm
from .forms import StaffRegistrationForm
from order.models import Order
from customer.models import Customer
class RegisterView(FormView):

    """View for staff registration."""

    template_name = "staff/register.html"
    form_class = StaffRegistrationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """if registration is successful"""
        form.save()
        messages.success(self.request, "Staff registered successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """if registration is not successful"""
        messages.error(self.request, "There was an error in the registration form.")
        return super().form_invalid(form)


class LoginView(View):

    """View for staff login."""

    template_name = "login.html"

    def get(self, request):
        """render the login page"""
        return render(request, self.template_name)

    def post(self, request):
        """if login is successful"""
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        user = authenticate(
            request,
            phone_number=phone_number,
            password=password,
            backend="staff.auth.PhoneNumberBackend",
        )

        if user :
            login(request, user)
            return render(request,'staff.html',{'user':user,'login_logout':'logout'})
        else:
            messages.error(request, "Invalid phone number or password.")
            return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    """Handle staff logout."""

    def get(self, request):
        """if logout is successful"""
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return render (request,'staff.html',{'login_logout':'login'})


@method_decorator(login_required, name="dispatch")
class StaffView(View):
    """Render the staff page."""

    template_name = "staff.html"

    def get(self, request):

        if request.user.is_authenticated:
            """render the staff page"""
        # context = self.get_context_data()
            return render(request, self.template_name,{'login_logout':'logout'})
        else:
            return render(request, self.template_name,{'login_logout':'login'})
    def get_context_data(self, **kwargs):
        context = {}
        return context
    # def get_context_data(self, **kwargs):
    #     """get the context data"""
    #     context = super().get_context_data(
    #         **kwargs
    #     )  # Call the parent method to get existing context
    #     # Add any additional context data here if needed
    #     return context
    
class OrderFilterView(View):
    template_name = 'staff\order_list.html'

    def get(self, request):
        form = OrderFilterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            filter_type = form.cleaned_data['filter_type']
            filter_value= form.cleaned_data['filter_value']
            if filter_type!='last_order' and filter_value =='':
                form.add_error('filter_value', 'Please enter a valid value.')

            elif filter_type == 'last_order' :
                orders = View.Order.objects.order_by('-order_date')[:1]  # Last order
                return render(request, self.template_name, {'form': form, 'orders': orders})

            elif filter_type !='last_order' and filter_value!='':
            
            # Apply filtering based on filter type
                if filter_type == 'date':
                    import datetime
                    try:
                        date_filter = datetime.datetime.strptime(filter_value, '%Y-%m-%d')
                        orders = Order.objects.filter(order_date__date=date_filter)
                    except ValueError:
                        orders =Order.objects.none()  # Return no results on invalid date
                elif filter_type == 'status':
                    orders = Order.objects.filter(status=filter_value)
                elif filter_type == 'table_number':
                    customers = Customer.objects.filter(table_number=filter_value)
                    orders = Order.objects.filter(customer__in=customers)

                return render(request, self.template_name, {'form': form, 'orders': orders})
        
            return render(request, self.template_name, {'form': form})
        

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
