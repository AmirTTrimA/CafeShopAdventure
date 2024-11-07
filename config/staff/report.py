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
from django.http import HttpResponse
from django.views import View
from .models import Staff
from django.urls import reverse_lazy
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.contrib.auth.decorators import user_passes_test

# from openpyxl import Workbook
from order.models import Order, OrderItem
from customer.models import Customer
from menu.models import MenuItem, Category
from .forms import OrderFilterForm, DataAnalysisForm, SaleAnalysisForm
from .forms import StaffRegistrationForm


class ReportView(View):
    """
    A class that generates various reports related to sales, customer demographics,
    and orders for a specific period.
    """

    def top_products(self):
        """
        Retrieves the top 5 products sold in the last month.

        Returns:
            QuerySet: A queryset containing the top products with their names,
            prices, total orders, and total sales amount.
        """
        now = timezone.now()
        last_month_start = now - timedelta(days=30)
        # start_of_month = now.replace(day=1)
        # # end_of_month = (start_of_month + timezone.timedelta(days=31)).replace(day=1)

        top_products = (
            OrderItem.objects.filter(created_at__gte=last_month_start)
            .values("item__name", "item__price")
            .annotate(total_orders=Sum("quantity"))
            .annotate(total_price=Sum("quantity") * F("item__price"))
            .order_by("-total_orders")[:5]
        )

        return top_products

    def peak_business_hour(self):
        """
        Analyzes peak business hours based on orders extracted from the last month.

        Returns:
            dict: A dictionary containing the most frequent hour of orders per day
            and overall most frequent hour across all days in the last month.
        """
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
        return orders

    def customer_demographic_data(self):
        """
        Collects demographic data regarding customers based on age and gender.

        Returns:
            dict: A dictionary summarizing customer counts by gender and age group.
        """
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
        return context

    def total_sales(self):
        """
        Computes total sales data including individual items and overall totals.

        Returns:
            dict: A dictionary containing sales data for each item
            and the overall sales cost and count.
        """
        sales_data = (
            OrderItem.objects.filter(order__status="Completed")
            .values("item__name")
            .annotate(total_quantity=Sum("quantity"), total_cost=Sum("subtotal"))
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
        return context

    def daily_sales(self):
        """
        Retrieves daily sales figures across all completed orders.

        Returns:
            dict: A dictionary containing daily total sales and product sales
            data organized by date.
        """
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
            .annotate(total_quantity=Sum("quantity"), total_sales=Sum("subtotal"))
        )

        product_sales_data = defaultdict(
            lambda: defaultdict(lambda: {"total_quantity": 0, "total_sales": 0})
        )

        for product_sales in sales_data:
            date = product_sales["date"]
            product_name = product_sales["item__name"]
            product_sales_data[date][product_name]["total_quantity"] += product_sales[
                "total_quantity"
            ]
            product_sales_data[date][product_name]["total_sales"] += product_sales[
                "total_sales"
            ]

        context = {
            "daily_total_sales": results,
            "daily_product_sales": sales_data,
            "daily_sortbydate": product_sales_data,
        }

        return context

    def monthly_sales(self):
        """
        Retrieves monthly sales figures across all completed orders.

        Returns:
            dict: A dictionary containing daily total sales and product sales
            data organized by date.
        """
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
            .annotate(total_quantity=Sum("quantity"), total_sales=Sum("subtotal"))
        )

        product_sales_data = defaultdict(
            lambda: defaultdict(lambda: {"total_quantity": 0, "total_sales": 0})
        )

        for product_sales in sales_data:
            date = product_sales["date"]
            product_name = product_sales["item__name"]
            product_sales_data[date][product_name]["total_quantity"] += product_sales[
                "total_quantity"
            ]
            product_sales_data[date][product_name]["total_sales"] += product_sales[
                "total_sales"
            ]

        context = {
            "daily_total_sales": results,
            "daily_product_sales": sales_data,
            "daily_sortbydate": product_sales_data,
        }

        return context

    def yearly_sales(self):
        """
        Retrieves yearly sales figures across all completed orders.

        Returns:
            dict: A dictionary containing daily total sales and product sales
            data organized by date.
        """
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
            .annotate(total_quantity=Sum("quantity"), total_sales=Sum("subtotal"))
        )

        product_sales_data = defaultdict(
            lambda: defaultdict(lambda: {"total_quantity": 0, "total_sales": 0})
        )

        for product_sales in sales_data:
            date = product_sales["date"]
            product_name = product_sales["item__name"]
            product_sales_data[date][product_name]["total_quantity"] += product_sales[
                "total_quantity"
            ]
            product_sales_data[date][product_name]["total_sales"] += product_sales[
                "total_sales"
            ]

        context = {
            "daily_total_sales": results,
            "daily_product_sales": sales_data,
            "daily_sortbydate": product_sales_data,
        }

        return context

    def customer_analytics(self):
        """
        Retrieves the top 5 customers based on their order activity within the last month.

        This function filters orders from the last 30 days, aggregates the number of orders
        and total spending for each customer, and sorts them in descending order of total
        spent and number of orders. It then retrieves the associated points of each top customer
        based on their phone number.

        Returns:
            list: A list of dictionaries, each containing the customer's phone number,
                  number of orders, total spent, and loyalty points.
        """
        now = timezone.now()
        last_month_start = now - timedelta(days=30)

        # Get the top 5 customers by number of orders and total spent
        top_customers = (
            Order.objects.filter(order_date__gte=last_month_start)
            .values("customer__phone_number")
            .annotate(number_of_orders=Count("id"), total_spent=Sum("total_price"))
            .order_by("-total_spent", "-number_of_orders")[:5]
        )

        # for customer in top_customers:
        #     customer_obj = Customer.objects.get(phone_number=customer['customer__phone_number'])
        #     customer['points'] = customer_obj.points

        return top_customers
