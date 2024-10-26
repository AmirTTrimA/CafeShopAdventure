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
from menu.models import MenuItem, Category
from .forms import OrderFilterForm
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
    template_name = "order_list.html"

    def get(self, request):
        form = OrderFilterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OrderFilterForm()
        if request.POST.get('form_type')=='change_status':
            data=request.POST
            order_id=data.get('order_id')
            print(order_id)
            new_status=data.get('status')
            order = Order.objects.get(id=order_id)
            order.status=new_status
            order.save()
            return render(request, self.template_name, {"form": form,'massage':'Status change was done successfully'})
        else:
            form = OrderFilterForm(request.POST)
            if form.is_valid():
                filter_type = form.cleaned_data["filter_type"]
                filter_value = form.cleaned_data["filter_value"]
                if filter_type != "last_order" and filter_value == "":
                    form.add_error("filter_value", "Please enter a valid value.")

                elif filter_type == "last_order":
                    orders = Order.objects.order_by("-order_date")[:1]  # Last order
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
    


class EditProduct(View):

    def get(self, request):
        items = MenuItem.objects.all()
        cats = Category.objects.all()
        return render(
            request, "edit-product.html", {"massage": "", "items": items, "cats": cats}
        )

    def post(self, request):
         name_e=request.POST.get('Product')
         name_i = request.POST.get('Prodcut Name')
         item=MenuItem.objects.get(name=name_e)
         items=MenuItem.objects.all()
         cats=Category.objects.all()
         if item:
            if name_i is not '':
                item.name=name_i
            price =request.POST.get('Product Price')
            if price is not '':
                item.price=Decimal(price)
            item_cat = request.POST.get('Product cat')
            if item_cat is not ['']:
                item.category=Category.objects.get(id=item_cat)
            if request.POST.get("Product description") is not ['']:
                item.description=request.POST.get("Product description")
            item.save()
            return render(request,'Edit-product.html',{'items':items,'cats':cats,'massage':'Changes saved successfully'})
         else:
            return render(request,'Edit-product.html',{'items':items,'cats':cats,'massage':'product dose not exist'})
        
class Add_product(View):

    def get(self, request):
        cats=Category.objects.all()
        return render(request, "add-product.html",{'cats':cats})
    
    def post(self, request):
        data=request.POST
        cats=Category.objects.all()
        Product_Name=(data.getlist('Prodcut Name'))[0]
         
        Product_cat=(data.getlist('Product cat'))[0]
        category_p=Category.objects.get(id=Product_cat)
        Product_description = data.get('Product description')
        Product_Price=data.get('Product Price')
        check_item=MenuItem.objects.filter(name=Product_Name,category=category_p)
        if check_item:
            return render(request, "add-product.html",{'cats':cats,'massage':'There is a product with this title and category'})
        else:
            item=MenuItem.objects.create(name=Product_Name,description=Product_description,price=Decimal(Product_Price),category=category_p)
            item.save()
            return render(request, "add-product.html",{'cats':cats,'massage':'saved!!'})

class RemoveProduct(View):
    def get(self, request):
        cats=Category.objects.all()
        return render(request, "remove-p.html",{'cats':cats})
    
    def post(self, request):
        data=request.POST
        cats=Category.objects.all()
        Product_Name=(data.getlist('Prodcut Name'))[0]
        Product_cat=(data.getlist('Product cat'))[0]
        category_p=Category.objects.get(id=Product_cat)
        item=MenuItem.objects.filter(name=Product_Name,category=category_p)
        if item:
            item.delete()
            return render(request, "remove-p.html",{'cats':cats,'massage':'Product removal was successful'})
        else:
             return render(request, "remove-p.html",{'cats':cats,'massage':'this product dose not exist!'})
        
class AddCategory(View):
    def get(self, request):
        return render(request, "Add-category.html")
    
    def post(self, request):
        data=request.POST
        Category_Name=data.get('Category Name')
        item=Category.objects.filter(name=Category_Name)
        if item:
            return render(request, "Add-category.html",{'massage':'There is a category with this title'})
        else:
            new_item=Category.objects.create(name=Category_Name)
            new_item.save()
            return render(request, "Add-category.html",{'massage':'Information saved successfully'})
    
class RemoveCategory(View):
    def get(self, request):
        return render(request, "remove-c.html")
    
    def post(self, request):
        data=request.POST
        Category_Name=data.get('Category Name')
        item=Category.objects.filter(name=Category_Name)
        if item:
            item.delete()

            return render(request, "Add-category.html",{'massage':'Information saved successfully'})
        else:
            return render(request, "Add-category.html",{'massage':'There is no category with this title'})
    
