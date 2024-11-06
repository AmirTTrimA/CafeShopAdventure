from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from order.models import Order
from .models import SalesAnalytics

class CustomerAnalyticsViewTest(TestCase):
    def test_customer_analytics_view_status_code(self):
        response = self.client.get(reverse('customer-analytics'))
        self.assertEqual(response.status_code, 200)
    
    def test_customer_analytics_template_used(self):
        response = self.client.get(reverse('customer-analytics'))
        self.assertTemplateUsed(response, 'customer-analytics.html')


class OrdersViewTest(TestCase):
    def test_orders_view_status_code(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
    
    def test_orders_template_used(self):
        response = self.client.get(reverse('orders'))
        self.assertTemplateUsed(response, 'orders.html')

class SalesAnalyticsModelTest(TestCase):
    def setUp(self):        
        # تاریخ تست
        self.test_date = timezone.now().date()
        
        # ایجاد سفارشات برای تاریخ تست
        Order.objects.create(order_date=self.test_date, total_price=100.00)
        Order.objects.create(order_date=self.test_date, total_price=200.00)
    
    def test_create_sales_analytics(self):
        # ایجاد یک رکورد SalesAnalytics
        analytics = SalesAnalytics(date=self.test_date)
        analytics.save()
        
        # بررسی اینکه آیا رکورد ایجاد شده است
        self.assertEqual(SalesAnalytics.objects.count(), 1)
    
    def test_calculate_totals(self):
        # ایجاد رکورد SalesAnalytics و بررسی مقادیر محاسبه شده
        analytics = SalesAnalytics(date=self.test_date)
        analytics.calculate_totals()
        
        # بررسی تعداد سفارشات
        self.assertEqual(analytics.total_orders, 2)
        
        # بررسی مجموع قیمت سفارشات
        self.assertEqual(analytics.total_sales, 300.00)

    def test_save_method_calculate_totals(self):
        # بررسی محاسبه اتوماتیک مقادیر در متد save
        analytics = SalesAnalytics(date=self.test_date)
        analytics.save()
        
        # بررسی تعداد سفارشات و مجموع قیمت پس از ذخیره
        self.assertEqual(analytics.total_orders, 2)
        self.assertEqual(analytics.total_sales, 300.00)
