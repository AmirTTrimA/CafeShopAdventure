import json
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from customer.models import Customer
from menu.models import MenuItem, Category
from staff.models import Staff
from .models import Order, OrderItem


class OrderViewTests(TestCase):
    def setUp(self):
        """ایجاد کاربر، دسته‌بندی و آیتم منو برای تست."""
        self.customer = Customer.objects.create(
            phone_number="09123456789", table_number="1"
        )
        self.staff_member = Staff.objects.create_user(
            phone_number="09123456788", password="testpassword"
        )
        self.category = Category.objects.create(name="Beverages")
        self.menu_item = MenuItem.objects.create(
            name="Coffee", price=Decimal("2.50"), category=self.category
        )
        self.client.login(
            phone_number="09123456788", password="testpassword"
        )  # لاگین کردن کاربر staff

    def test_add_to_cart_view(self):
        """Test adding an item to the cart."""
        response = self.client.get(
            reverse("add_to_cart", args=[self.menu_item.id]), {"quantity": 2}
        )
        self.assertEqual(response.status_code, 302)  # Update to match view response
        cart = json.loads(response.cookies["cart"].value)
        self.assertIn(str(self.menu_item.id), cart)
        self.assertEqual(cart[str(self.menu_item.id)]["quantity"], 2)

    def test_cart_view_empty_cart(self):
        self.client.get(
            reverse("remove_from_cart", args=[self.menu_item.id])
        )  # Remove item
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)  # Should render cart view
        self.assertContains(response, "Your cart is empty.")

    def test_order_success_view(self):
        """Test the order success page."""
        response = self.client.get(reverse("order_success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_success.html")

    def test_order_negative_total_price(self):
        """Test creating an order with a negative total price."""
        order = Order(
            customer=self.customer,
            table_number=self.customer.table_number,
            total_price=-50.0,  # Invalid total price
            status="Completed",
        )
        with self.assertRaises(ValidationError):
            order.full_clean()  # Should raise validation error

    def test_order_invalid_status(self):
        """Test creating an order with an invalid status."""
        order = Order(
            customer=self.customer,
            table_number=self.customer.table_number,
            total_price=100.0,
            status="InvalidStatus",  # Invalid status
        )
        with self.assertRaises(ValidationError):
            order.full_clean()  # Should raise validation error

    def test_cart_functionality(self):
        """Test adding items to the cart and checking cart data."""
        response = self.client.get(
            reverse("add_to_cart", args=[self.menu_item.id]), {"quantity": 3}
        )

        # چک کردن وضعیت پاسخ
        self.assertEqual(response.status_code, 302)

        # بررسی ذخیره‌سازی سبد خرید در کوکی‌ها
        cart = json.loads(response.cookies["cart"].value)
        self.assertIn(str(self.menu_item.id), cart)
        self.assertEqual(cart[str(self.menu_item.id)]["quantity"], 3)

    def test_order_item_subtotal_calculation(self):
        """Test if subtotal for an order item is calculated correctly."""
        order = Order.objects.create(
            customer=self.customer, staff=self.staff_member, table_number="1"
        )
        order_item = OrderItem.objects.create(
            order=order, item=self.menu_item, quantity=3
        )
        self.assertEqual(order_item.subtotal, Decimal("7.50"))  # 2.50 * 3

    def test_order_update_total_price_on_item_change(self):
        """Test if the total price of an order updates when an order item is changed."""
        order = Order.objects.create(
            customer=self.customer, staff=self.staff_member, table_number="1"
        )
        order_item = OrderItem.objects.create(
            order=order, item=self.menu_item, quantity=1
        )
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal("2.50"))  # Initial total price

        # Change the quantity of the order item
        order_item.quantity = 4
        order_item.save()  # This should trigger total price recalculation
        self.assertEqual(order.total_price, Decimal("10.00"))  # 2.50 * 4

    def test_order_item_removal_updates_total_price(self):
        """Test if removing an order item updates the total price."""
        order = Order.objects.create(
            customer=self.customer, staff=self.staff_member, table_number="1"
        )
        order_item1 = OrderItem.objects.create(
            order=order, item=self.menu_item, quantity=2
        )
        order_item2 = OrderItem.objects.create(
            order=order, item=self.menu_item, quantity=1
        )
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal("7.50"))  # 2.50 * 2 + 2.50 * 1

        # Remove one item
        order_item1.delete()
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal("2.50"))  # Only one item left

    def tearDown(self):
        self.customer.delete()
        self.staff_member.delete()
        self.menu_item.delete()
        self.category.delete()
        Order.objects.all().delete()
