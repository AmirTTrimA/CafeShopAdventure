from django.test import TestCase
from django.urls import reverse
from .models import Order
from customer.models import Customer
from menu.models import MenuItem, Category
from staff.models import Staff
from decimal import Decimal
import json
from django.core.exceptions import ValidationError


class OrderViewTests(TestCase):

    def setUp(self):
        """ایجاد کاربر، دسته‌بندی و آیتم منو برای تست."""
        self.customer = Customer.objects.create(phone_number="09123456789", table_number="1")
        self.staff_member = Staff.objects.create_user(phone_number="09123456788", password="testpassword")
        self.category = Category.objects.create(name="Beverages")
        self.menu_item = MenuItem.objects.create(name="Coffee", price=Decimal("2.50"), category=self.category)
        self.client.login(phone_number="09123456788", password="testpassword")  # لاگین کردن کاربر staff

    def test_add_to_cart_view(self):
        """Test adding an item to the cart."""
        response = self.client.get(reverse('add_to_cart', args=[self.menu_item.id]), {'quantity': 2})
        self.assertEqual(response.status_code, 200)  # Change to 200 for handling in view
        cart = json.loads(response.cookies['cart'].value)
        self.assertIn(str(self.menu_item.id), cart)
        self.assertEqual(cart[str(self.menu_item.id)]['quantity'], 2)

    def test_submit_order_view(self):
        """Test submitting an order."""
        self.client.cookies['cart'] = json.dumps({str(self.menu_item.id): {"quantity": 2}})
        response = self.client.post(reverse('submit_order'), {'table_number': '5', 'phone_number': '09123456789'})
        self.assertEqual(response.status_code, 302)  # Redirect response
        order = Order.objects.last()
        self.assertEqual(order.customer.phone_number, '09123456789')
        self.assertEqual(order.total_price, Decimal("5.00"))  # 2 * 2.50

    def test_order_success_view(self):
        """Test the order success page."""
        response = self.client.get(reverse('order_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_success.html')
    
    def test_order_negative_total_price(self):
        """Test creating an order with a negative total price."""
        order = Order(
            customer=self.customer,
            table_number=self.customer.table_number,
            total_price=-50.0,  # Invalid total price
            status='Completed'
        )
        with self.assertRaises(ValidationError):
            order.full_clean()  # Should raise validation error

    def test_order_invalid_status(self):
        """Test creating an order with an invalid status."""
        order = Order(
            customer=self.customer,
            table_number=self.customer.table_number,
            total_price=100.0,
            status='InvalidStatus'  # Invalid status
        )
        with self.assertRaises(ValidationError):
            order.full_clean()  # Should raise validation error

    # def test_order_invalid_table_number(self):
    #     """Test creating an order with a table number that doesn't exist."""
    #     order = Order(
    #         customer=self.customer,
    #         table_number=50,  # Invalid table number (assuming the cafe only has 10 tables)
    #         total_price=100.0,
    #         status='Completed'
    #     )
    #     with self.assertRaises(ValidationError):
    #         order.full_clean()  # Should raise validation error


    def test_manage_order_items_view(self):
        # ایجاد سفارش برای customer در تست
        order = Order.objects.create(customer=self.customer)
        
        response = self.client.get(reverse('order_list', args=[order.id]))
        
        # چک کردن کد وضعیت به جای ریدایرکت و انتظار کد 200
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.customer.delete()
        self.staff_member.delete()
        self.menu_item.delete()
        self.category.delete()
        Order.objects.all().delete()
    