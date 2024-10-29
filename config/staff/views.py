"""views.py"""

from decimal import Decimal
from collections import defaultdict
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse_lazy
from order.models import Order,OrderItem
from customer.models import Customer
from menu.models import MenuItem, Category
from .forms import OrderFilterForm,DataAnalysisForm
from .forms import StaffRegistrationForm
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Count
from collections import Counter
from django.db.models.functions import TruncHour, TruncDay
from datetime import timedelta,date
from django.db import models


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
        if request.POST.get("form_type") == "change_status":
            data = request.POST
            order_id = data.get("order_id")
            print(order_id)
            new_status = data.get("status")
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return render(
                request,
                self.template_name,
                {"form": form, "massage": "Status change was done successfully"},
            )
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
        name_e = request.POST.get("Product")
        name_i = request.POST.get("Prodcut Name")
        item = MenuItem.objects.get(name=name_e)
        items = MenuItem.objects.all()
        cats = Category.objects.all()
        if item:
            if name_i != "":
                item.name = name_i
            price = request.POST.get("Product Price")
            if price != "":
                item.price = Decimal(price)
            item_cat = request.POST.get("Product cat")
            if item_cat is not [""]:
                item.category = Category.objects.get(id=item_cat)
            if request.POST.get("Product description") is not [""]:
                item.description = request.POST.get("Product description")
            item.save()
            return render(
                request,
                "Edit-product.html",
                {"items": items, "cats": cats, "massage": "Changes saved successfully"},
            )
        else:
            return render(
                request,
                "Edit-product.html",
                {"items": items, "cats": cats, "massage": "product dose not exist"},
            )


class Add_product(View):
    def get(self, request):
        cats = Category.objects.all()
        return render(request, "add-product.html", {"cats": cats})

    def post(self, request):
        data = request.POST
        cats = Category.objects.all()
        product_name = (data.getlist("Prodcut Name"))[0]

        product_cat = (data.getlist("Product cat"))[0]
        category_p = Category.objects.get(id=product_cat)
        product_description = data.get("Product description")
        product_price = data.get("Product Price")
        check_item = MenuItem.objects.filter(name=product_name, category=category_p)
        if check_item:
            return render(
                request,
                "add-product.html",
                {
                    "cats": cats,
                    "massage": "There is a product with this title and category",
                },
            )
        else:
            item = MenuItem.objects.create(
                name=product_name,
                description=product_description,
                price=Decimal(product_price),
                category=category_p,
            )
            item.save()
            return render(
                request, "add-product.html", {"cats": cats, "massage": "saved!!"}
            )


class RemoveProduct(View):
    def get(self, request):
        cats = Category.objects.all()
        pros=MenuItem.objects.all()
        return render(request, "remove-p.html", {"cats": cats,"product":pros})

    def post(self, request):
        data = request.POST
        cats = Category.objects.all()
        pros=MenuItem.objects.all()
        print(pros)
        product_name = (data.get("Product Name"))
        product_cat = (data.get("Product cat"))
        category_p = Category.objects.get(id=product_cat)
        item = MenuItem.objects.filter(name=product_name, category=category_p)
        if item:
            item.delete()
            return render(
                request,
                "remove-p.html",
                {"cats": cats,"product":pros, "massage": "Product removal was successful"},
            )
        else:
            return render(
                request,
                "remove-p.html",
                {"cats": cats,"product":pros, "massage": "this product dose not exist!"},
            )


class AddCategory(View):
    def get(self, request):
        return render(request, "Add-category.html")

    def post(self, request):
        data = request.POST
        category_name = data.get("Category Name")
        item = Category.objects.filter(name=category_name)
        if item:
            return render(
                request,
                "Add-category.html",
                {"massage": "There is a category with this title"},
            )
        else:
            new_item = Category.objects.create(name=category_name)
            new_item.save()
            return render(
                request,
                "Add-category.html",
                {"massage": "Information saved successfully"},
            )


class RemoveCategory(View):
    def get(self, request):
        return render(request, "remove-c.html")

    def post(self, request):
        data = request.POST
        category_name = data.get("Category Name")
        item = Category.objects.filter(name=category_name)
        if item:
            item.delete()

            return render(
                request,
                "Add-category.html",
                {"massage": "Information saved successfully"},
            )
        else:
            return render(
                request,
                "Add-category.html",
                {"massage": "There is no category with this title"},
            )
          
          
def staff_checkout(request):
    orders = Order.objects.all()
    print(f"orders: {orders}")
    return render(request, "checkout.html", {"orders": orders})


def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        return redirect("checkout")


def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()
    products = MenuItem.objects.all()

    return render(
        request,
        "order_list.html",
        {"order": order, "order_items": order_items, "products": products},
    )


def add_order_item(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))

        product = get_object_or_404(MenuItem, id=product_id)
        order_item, created = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        if not created:
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity

        order_item.save()
        return redirect("order_list", order_id=order.id)


def update_order_item(request, item_id):
    if request.method == "POST":
        order_item = get_object_or_404(OrderItem, id=item_id)
        new_quantity = int(request.POST.get("quantity"))

        if new_quantity > 0:
            order_item.quantity = new_quantity
            order_item.save()
        else:
            order_item.delete()

        return redirect("order_list", order_id=order_item.order.id)


def remove_order_item(request, item_id):
    if request.method == "POST":
        order_item = get_object_or_404(OrderItem, id=item_id)
        order_item.delete()
        return redirect("order_list", order_id=order_item.order.id)

class ViewManager(View):
     def get(self, request):
        return render(request, "Manager.html")

class StaffAccess(View):
     def get(self, request):
        return render(request, "staff-access.html")

class DataAnalysis(View):
    
    def get(self, request):
        form = DataAnalysisForm()
        return render(request,"data_analysis.html",{'form': form})
    def post(self,request):
        form = DataAnalysisForm(request.POST)
        now = timezone.now()
        if form.is_valid():
            filter_type = form.cleaned_data["filter_type"]
            if filter_type == "most popular caffe items":
                now = timezone.now()
                last_month_start = now - timedelta(days=30)
                start_of_month = now.replace(day=1)
                # end_of_month = (start_of_month + timezone.timedelta(days=31)).replace(day=1)

                top_products = (
                OrderItem.objects
                .filter(created_at__gte=last_month_start)
                .values('item__name')
                .annotate(total_orders=Sum('quantity'))
                .order_by('-total_orders')[:5]
                )
                print(top_products)
                return render(request,"data_analysis.html",{'form': form,'orders':top_products})
            

            elif filter_type == "peak business hour":
                now = timezone.now()
                last_month_start = now - timedelta(days=30)

                # Filter orders from the last month
                orders = Order.objects.filter(created_at__gte=last_month_start)

                # Extract the hour and day of the week from the orders
                order_times = defaultdict(lambda: defaultdict(int))

                # Iterate through orders and count occurrences of hour per day
                for order in orders:
                    day = order.created_at.strftime('%A')  # Get day of the week
                    hour = order.created_at.strftime('%H')  # Get hour
                    order_times[day][hour] += 1

                    # Calculate most frequent hours per day of the week
                    most_frequent_per_day = {}
                    total_orders = orders.count()
                    overall_count = defaultdict(int)

                for day, timestamps in order_times.items():
                    most_frequent_hour = max(timestamps.items(), key=lambda x: x[1], default=(None, 0))
                    most_frequent_per_day[day] = {
                    'hour': most_frequent_hour[0],
                    'count': most_frequent_hour[1]
                    }
        
                # Aggregate for overall most frequent hour
                if most_frequent_hour[0] is not None:
                    overall_count[most_frequent_hour[0]] += most_frequent_hour[1]

                # Calculate the overall most frequent hour in the last month
                overall_most_frequent_hour = max(overall_count.items(), key=lambda x: x[1], default=(None, 0))

                orders = {
                    'most_frequent_per_day': most_frequent_per_day,
                    'overall_most_frequent_hour': {
                    'hour': overall_most_frequent_hour[0],
                    'total_orders': overall_most_frequent_hour[1],
                    'total_orders_month': total_orders,
                    },
                    }
                return render(request,"data_analysis.html", {"form":form,'orders':orders})

            elif filter_type =="customer demographic data" :
                
                today = date.today()
                under_20_females = Customer.objects.filter(
                gender='female', 
                date_of_birth__gte=today.replace(year=today.year - 20)
                ).count()

                between_20_and_40_females = Customer.objects.filter(
                gender='female', 
                date_of_birth__lt=today.replace(year=today.year - 20),
                date_of_birth__gte=today.replace(year=today.year - 40)
                ).count()

                over_40_females = Customer.objects.filter(
                gender='female', 
                date_of_birth__lt=today.replace(year=today.year - 40)
                ).count()

                under_20_Uncertain = Customer.objects.filter(
                gender='Uncertain', 
                date_of_birth__gte=today.replace(year=today.year - 20)
                ).count()

                between_20_and_40_Uncertain = Customer.objects.filter(
                gender='Uncertain', 
                date_of_birth__lt=today.replace(year=today.year - 20),
                date_of_birth__gte=today.replace(year=today.year - 40)
                ).count()

                over_40_Uncertain = Customer.objects.filter(
                gender='Uncertain', 
                date_of_birth__lt=today.replace(year=today.year - 40)
                ).count()

                under_20_males = Customer.objects.filter(
                gender='man', 
                date_of_birth__gte=today.replace(year=today.year - 20)
                ).count()

                between_20_and_40_males = Customer.objects.filter(
                gender='man', 
                date_of_birth__lt=today.replace(year=today.year - 20),
                date_of_birth__gte=today.replace(year=today.year - 40)
                ).count()

                over_40_males = Customer.objects.filter(
                gender='man', 
                date_of_birth__lt=today.replace(year=today.year - 40)
                ).count()

                # Prepare context for rendering in a template
                context = {
                'under_20_Uncertain': under_20_Uncertain,
                'between_20_and_40_Uncertain': between_20_and_40_Uncertain,
                'over_40_Uncertain':over_40_Uncertain,
                'under_20_females': under_20_females,
                'between_20_and_40_females': between_20_and_40_females,
                'over_40_females': over_40_females,
                'under_20_males': under_20_males,
                'between_20_and_40_males': between_20_and_40_males,
                'over_40_males': over_40_males,
                'year': today.year,
                }
                print(context)
                return render(request, 'data_analysis.html', {'form':form,'orders':context})
            else:
                form.add_error("filter_type", "Please enter a valid value.")

class SalesAnalysis(View):
    def get(self, request):
        form = OrderFilterForm()
        return render(request, "Manager.html",{'form':form})
    def post(self,request):
        pass

@user_passes_test(lambda u: u.is_staff)
def search_customer(request):
    customers = []
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number', '')
        if phone_number:
            customers = Customer.objects.filter(phone_number=phone_number)
    return render(request, 'staff/search_customer.html', {'customers': customers})      
