"""views.py"""

from decimal import Decimal
from datetime import timedelta, date
from collections import defaultdict
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from django.utils import timezone
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.contrib.auth.decorators import user_passes_test
from order.models import Order, OrderItem
from customer.models import Customer
from menu.models import MenuItem, Category
from .forms import OrderFilterForm, DataAnalysisForm, SaleAnalysisForm
from .forms import StaffRegistrationForm


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
            order_id = data.get("order_id") or 1  # Default to 1 if not provided
            new_status = (
                data.get("status") or "pending"
            )  # Default to "pending" if not provided

            try:
                order = Order.objects.get(id=order_id)
                order.status = new_status
                order.save()
                return render(
                    request,
                    self.template_name,
                    {"form": form, "message": "Status change was done successfully"},
                )
            except Order.DoesNotExist:
                return render(
                    request,
                    self.template_name,
                    {"form": form, "error": "Order not found."},
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

                    # Ensure we have an order to work with
                    if orders.exists():
                        order = (
                            orders.first()
                        )  # Get the first order from the filtered results
                    else:
                        order = None  # No orders found

                    return render(
                        request,
                        self.template_name,
                        {"form": form, "orders": orders, "order": order},
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
            if item_cat != [""]:
                item.category = Category.objects.get(id=item_cat)
            if request.POST.get("Product description") != [""]:
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
        pros = MenuItem.objects.all()
        return render(request, "remove-p.html", {"cats": cats, "product": pros})

    def post(self, request):
        data = request.POST
        cats = Category.objects.all()
        pros = MenuItem.objects.all()
        print(pros)
        product_name = data.get("Product Name")
        product_cat = data.get("Product cat")
        category_p = Category.objects.get(id=product_cat)
        item = MenuItem.objects.filter(name=product_name, category=category_p)
        if item:
            item.delete()
            return render(
                request,
                "remove-p.html",
                {
                    "cats": cats,
                    "product": pros,
                    "massage": "Product removal was successful",
                },
            )
        else:
            return render(
                request,
                "remove-p.html",
                {
                    "cats": cats,
                    "product": pros,
                    "massage": "this product dose not exist!",
                },
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


# class EditCategory(View):
#     def get(self, request, category_id):
#         category = get_object_or_404(Category, id=category_id)
#         form = CategoryForm(instance=category)  # بارگذاری فرم با داده‌های دسته‌بندی
#         return render(request, "edit_category.html", {"form": form, "category": category})

#     def post(self, request, category_id):
#         category = get_object_or_404(Category, id=category_id)
#         form = CategoryForm(request.POST, instance=category)  # بارگذاری فرم با داده‌های POST

#         if form.is_valid():
#             form.save()  # ذخیره تغییرات
#             messages.success(request, "Category updated successfully!")
#             return redirect("some_view_name")  # تغییر نام به نمای مناسب

#         return render(request, "edit_category.html", {"form": form, "category": category})


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
    # When each satff change the status, they will be that order's staff
    orders = Order.objects.all()
    return render(request, "checkout.html", {"orders": orders})


def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        return redirect("staff_checkout")


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


class StaffAccess(FormView):
    template_name = "staff-access.html"
    form_class = StaffRegistrationForm
    success_url = reverse_lazy("manager")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Staff registered successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in the registration form.")
        return super().form_invalid(form)


class DataAnalysis(View):
    def get(self, request):
        form = DataAnalysisForm()
        return render(request, "data_analysis.html", {"form": form})

    def post(self, request):
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
                    OrderItem.objects.filter(created_at__gte=last_month_start)
                    .values("item__name")
                    .annotate(total_orders=Sum("quantity"))
                    .order_by("-total_orders")[:5]
                )
                print(top_products)
                return render(
                    request,
                    "data_analysis.html",
                    {"form": form, "orders": top_products},
                )

            elif filter_type == "peak business hour":
                now = timezone.now()
                last_month_start = now - timedelta(days=30)

                # Filter orders from the last month
                orders = Order.objects.filter(created_at__gte=last_month_start)

                # Extract the hour and day of the week from the orders
                order_times = defaultdict(lambda: defaultdict(int))

                # Iterate through orders and count occurrences of hour per day
                for order in orders:
                    day = order.created_at.strftime("%A")  # Get day of the week
                    hour = order.created_at.strftime("%H")  # Get hour
                    order_times[day][hour] += 1

                    # Calculate most frequent hours per day of the week
                    most_frequent_per_day = {}
                    total_orders = orders.count()
                    overall_count = defaultdict(int)

                for day, timestamps in order_times.items():
                    most_frequent_hour = max(
                        timestamps.items(), key=lambda x: x[1], default=(None, 0)
                    )
                    most_frequent_per_day[day] = {
                        "hour": most_frequent_hour[0],
                        "count": most_frequent_hour[1],
                    }

                # Aggregate for overall most frequent hour
                if most_frequent_hour[0] is not None:
                    overall_count[most_frequent_hour[0]] += most_frequent_hour[1]

                # Calculate the overall most frequent hour in the last month
                overall_most_frequent_hour = max(
                    overall_count.items(), key=lambda x: x[1], default=(None, 0)
                )

                orders = {
                    "most_frequent_per_day": most_frequent_per_day,
                    "overall_most_frequent_hour": {
                        "hour": overall_most_frequent_hour[0],
                        "total_orders": overall_most_frequent_hour[1],
                        "total_orders_month": total_orders,
                    },
                }
                return render(
                    request, "data_analysis.html", {"form": form, "orders": orders}
                )

            elif filter_type == "customer demographic data":
                today = date.today()
                under_20_females = Customer.objects.filter(
                    gender="female",
                    date_of_birth__gte=today.replace(year=today.year - 20),
                ).count()

                between_20_and_40_females = Customer.objects.filter(
                    gender="female",
                    date_of_birth__lt=today.replace(year=today.year - 20),
                    date_of_birth__gte=today.replace(year=today.year - 40),
                ).count()

                over_40_females = Customer.objects.filter(
                    gender="female",
                    date_of_birth__lt=today.replace(year=today.year - 40),
                ).count()

                under_20_Uncertain = Customer.objects.filter(
                    gender="Uncertain",
                    date_of_birth__gte=today.replace(year=today.year - 20),
                ).count()

                between_20_and_40_Uncertain = Customer.objects.filter(
                    gender="Uncertain",
                    date_of_birth__lt=today.replace(year=today.year - 20),
                    date_of_birth__gte=today.replace(year=today.year - 40),
                ).count()

                over_40_Uncertain = Customer.objects.filter(
                    gender="Uncertain",
                    date_of_birth__lt=today.replace(year=today.year - 40),
                ).count()

                under_20_males = Customer.objects.filter(
                    gender="man", date_of_birth__gte=today.replace(year=today.year - 20)
                ).count()

                between_20_and_40_males = Customer.objects.filter(
                    gender="man",
                    date_of_birth__lt=today.replace(year=today.year - 20),
                    date_of_birth__gte=today.replace(year=today.year - 40),
                ).count()

                over_40_males = Customer.objects.filter(
                    gender="man", date_of_birth__lt=today.replace(year=today.year - 40)
                ).count()

                # Prepare context for rendering in a template
                context = {
                    "under_20_Uncertain": under_20_Uncertain,
                    "between_20_and_40_Uncertain": between_20_and_40_Uncertain,
                    "over_40_Uncertain": over_40_Uncertain,
                    "under_20_females": under_20_females,
                    "between_20_and_40_females": between_20_and_40_females,
                    "over_40_females": over_40_females,
                    "under_20_males": under_20_males,
                    "between_20_and_40_males": between_20_and_40_males,
                    "over_40_males": over_40_males,
                    "year": today.year,
                }
                print(context)
                return render(
                    request, "data_analysis.html", {"form": form, "orders": context}
                )
            else:
                form.add_error("filter_type", "Please enter a valid value.")


class SalesAnalysis(View):
    def get(self, request):
        form = SaleAnalysisForm()
        return render(request, "sale_analysis.html", {"form": form})

    def post(self, request):
        now = timezone.now()
        form = SaleAnalysisForm(request.POST)

        if form.is_valid():
            filter_type = form.cleaned_data["filter_type"]
            if filter_type == "total sales":
                sales_data = (
                    OrderItem.objects.filter(order__status="Completed")
                    .values("item__name")
                    .annotate(
                        total_quantity=Sum("quantity"), total_cost=Sum("subtotal")
                    )
                )

                total_sales_cost = OrderItem.objects.filter(
                    order__status="Completed"
                ).aggregate(
                    total_sales_cost=Sum("subtotal") or 0,
                    total_sales_count=Sum("quantity"),
                )

                context = {
                    "sales_data": sales_data,
                    "total_sales_cost": total_sales_cost,
                }

                return render(
                    request, "sale_analysis.html", {"orders": context, "form": form}
                )

            elif filter_type == "daily sales":
                results = (
                    Order.objects.filter(status="Completed")
                    .annotate(date=TruncDate("created_at"))
                    .prefetch_related("order_items_set")
                    .values("date")
                    .annotate(
                        total_sales=Sum("order_items__subtotal"),
                        total_items=Sum("order_items__quantity"),
                    )
                )

                sales_data = (
                    OrderItem.objects.filter(order__status="Completed")
                    .annotate(date=TruncDate("created_at"))
                    .values("item__name", "date")
                    .annotate(
                        total_quantity=Sum("quantity"), total_sales=Sum("subtotal")
                    )
                )

                product_sales_data = defaultdict(
                    lambda: defaultdict(lambda: {"total_quantity": 0, "total_sales": 0})
                )

                for product_sales in sales_data:
                    date = product_sales["date"]
                    product_name = product_sales["item__name"]
                    product_sales_data[date][product_name]["total_quantity"] += (
                        product_sales["total_quantity"]
                    )
                    product_sales_data[date][product_name]["total_sales"] += (
                        product_sales["total_sales"]
                    )

                context = {
                    "daily_total_sales": results,
                    "daily_product_sales": sales_data,
                    "daily_sortbydate": product_sales_data,
                }
                return render(
                    request, "sale_analysis.html", {"form": form, "orders": context}
                )

            elif filter_type == "monthly sales":
                results = (
                    Order.objects.filter(status="Completed")
                    .annotate(date=TruncMonth("created_at"))
                    .prefetch_related("order_items_set")
                    .values("date")
                    .annotate(
                        total_sales=Sum("order_items__subtotal"),
                        total_items=Sum("order_items__quantity"),
                    )
                )

                sales_data = (
                    OrderItem.objects.filter(order__status="Completed")
                    .annotate(date=TruncMonth("created_at"))
                    .values("item__name", "date")
                    .annotate(
                        total_quantity=Sum("quantity"), total_sales=Sum("subtotal")
                    )
                )

                product_sales_data = defaultdict(
                    lambda: defaultdict(lambda: {"total_quantity": 0, "total_sales": 0})
                )

                for product_sales in sales_data:
                    date = product_sales["date"]
                    product_name = product_sales["item__name"]
                    product_sales_data[date][product_name]["total_quantity"] += (
                        product_sales["total_quantity"]
                    )
                    product_sales_data[date][product_name]["total_sales"] += (
                        product_sales["total_sales"]
                    )

                context = {
                    "daily_total_sales": results,
                    "daily_product_sales": sales_data,
                    "daily_sortbydate": product_sales_data,
                }
                return render(
                    request, "sale_analysis.html", {"form": form, "orders": context}
                )
            elif filter_type == "yearly sales":
                results = (
                    Order.objects.filter(status="Completed")
                    .annotate(date=TruncYear("created_at"))
                    .prefetch_related("order_items_set")
                    .values("date")
                    .annotate(
                        total_sales=Sum("order_items__subtotal"),
                        total_items=Sum("order_items__quantity"),
                    )
                )

                sales_data = (
                    OrderItem.objects.filter(order__status="Completed")
                    .annotate(date=TruncYear("created_at"))
                    .values("item__name", "date")
                    .annotate(
                        total_quantity=Sum("quantity"), total_sales=Sum("subtotal")
                    )
                )

                product_sales_data = defaultdict(
                    lambda: defaultdict(lambda: {"total_quantity": 0, "total_sales": 0})
                )

                for product_sales in sales_data:
                    date = product_sales["date"]
                    product_name = product_sales["item__name"]
                    product_sales_data[date][product_name]["total_quantity"] += (
                        product_sales["total_quantity"]
                    )
                    product_sales_data[date][product_name]["total_sales"] += (
                        product_sales["total_sales"]
                    )

                context = {
                    "daily_total_sales": results,
                    "daily_product_sales": sales_data,
                    "daily_sortbydate": product_sales_data,
                }
                return render(
                    request, "sale_analysis.html", {"form": form, "orders": context}
                )
            else:
                form.add_error("filter_type", "Please enter a valid value.")


@user_passes_test(lambda u: u.is_staff)
def search_customer(request):
    customers = []
    if request.method == "GET":
        phone_number = request.GET.get("phone_number", "")
        if phone_number:
            customers = Customer.objects.filter(phone_number=phone_number)
            # order = Order.objects.filter(customer__phone_number=phone_number)
    return render(request, "search_customer.html", {"customers": customers})


@login_required
def top_selling_items(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date", timezone.now() - timedelta(days=30))
        end_date = request.POST.get("end_date", timezone.now())
        orders = OrderItem.objects.filter(
            order__order_date__range=[start_date, end_date]
        )
        top_items = (
            orders.values("item__name")
            .annotate(total_sales=Sum("quantity"))
            .order_by("-total_sales")[:10]
        )
        print(top_items)
        return render(
            request, "reports/top_selling_items.html", {"top_items": top_items}
        )
    elif request.method == "GET":
        return render(request, "reports/top_selling_items.html")


def sales_by_category(request):
    sales = OrderItem.objects.values("item__category__name").annotate(
        total_sales=Sum("quantity")
    )
    return render(request, "reports/sales_by_category.html", {"sales": sales})


def sales_by_customer(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        customer_orders = Order.objects.filter(customer__phone_number=phone_number)
        return render(
            request, "reports/sales_by_customer.html", {"orders": customer_orders}
        )
    elif request.method == "GET":
        return render(request, "reports/sales_by_customer.html")


def sales_by_time_of_day(request):
    morning_sales = Order.objects.filter(order_date__hour__lt=12).aggregate(
        total_sales=Count("id")
    )
    afternoon_sales = Order.objects.filter(order_date__hour__gte=12).aggregate(
        total_sales=Count("id")
    )
    return render(
        request,
        "reports/sales_by_time_of_day.html",
        {"morning_sales": morning_sales, "afternoon_sales": afternoon_sales},
    )


def order_status_report(request):
    date = request.GET.get("date", timezone.now().date())
    orders = (
        Order.objects.filter(order_date__date=date)
        .values("status")
        .annotate(total=Count("id"))
    )
    return render(request, "reports/order_status_report.html", {"orders": orders})


def sales_by_employee_report(request):
    employee_sales = Order.objects.values(
        "staff__first_name", "staff__last_name"
    ).annotate(total_sales=Count("id"))
    return render(
        request,
        "reports/sales_by_employee_report.html",
        {"employee_sales": employee_sales},
    )


def customer_order_history_report(request):
    customer_id = request.GET.get("customer_id")
    orders = Order.objects.filter(customer_id=customer_id).order_by("-order_date")
    return render(
        request, "reports/customer_order_history_report.html", {"orders": orders}
    )
