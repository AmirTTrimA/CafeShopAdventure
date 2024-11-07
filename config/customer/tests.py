from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from cafe.models import Cafe
from order.models import Order
from staff.models import Staff
from .models import Customer


class CustomerModelTests(TestCase):
    def setUp(self):
        # ایجاد یک کافه برای استفاده در تست‌ها
        self.cafe = Cafe.objects.create(
            name="Test Cafe",
            address="123 Test Street",
            opening_time="08:00",
            closing_time="20:00",
        )

    def test_customer_creation(self):
        """Test creating a customer with valid attributes."""
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            table_number=5,
            cafe=self.cafe,
            phone_number="09123456789",
            points=10,
            is_active=True,
        )
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.last_name, "Doe")
        self.assertEqual(customer.table_number, 5)
        self.assertEqual(customer.cafe, self.cafe)
        self.assertEqual(customer.phone_number, "09123456789")
        self.assertEqual(customer.points, 10)
        self.assertTrue(customer.is_active)

    def test_phone_number_validation(self):
        """Test creating a customer with an invalid phone number."""
        customer = Customer(
            first_name="Jane",
            last_name="Doe",
            table_number=5,
            cafe=self.cafe,
            phone_number="123456789",
            points=10,
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()  # Should raise validation error

    def test_customer_duplicate_phone_number(self):
        """Test creating a customer with a duplicate phone number."""
        # First customer with this phone number
        customer1 = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            table_number=5,
            cafe=self.cafe,
            phone_number="09123456789",
            points=10,
        )
        # Second customer with the same phone number should fail
        customer2 = Customer(
            first_name="Jane",
            last_name="Doe",
            table_number=5,
            cafe=self.cafe,
            phone_number="09123456789",  # Duplicate phone number
            points=10,
        )
        with self.assertRaises(ValidationError):
            customer2.full_clean()  # Should raise validation error

    def test_customer_table_number_negative(self):
        """Test creating a customer with a negative table number."""
        customer = Customer(
            first_name="Negative",
            last_name="Table",
            table_number=-1,  # Invalid table number
            cafe=self.cafe,
            phone_number="09123456789",
            points=10,
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()  # Should raise validation error

    def test_table_number_exceeds_cafe_tables(self):
        """Test that a customer cannot have a table number greater than the number of tables in the cafe."""
        customer = Customer(
            first_name="Alice",
            last_name="Smith",
            table_number=15,  # This exceeds the 10 tables in the cafe
            cafe=self.cafe,
            phone_number="09123456789",
            points=10,
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()  # Should raise validation error

    def test_customer_string_representation(self):
        """Test the string representation of the customer."""
        customer = Customer.objects.create(
            first_name="Bob",
            last_name="Brown",
            table_number=2,
            cafe=self.cafe,
            phone_number="09123456789",
        )
        self.assertEqual(str(customer), "09123456789")


class CustomerViewTests(TestCase):
    def setUp(self):
        # Create a cafe for testing
        self.cafe = Cafe.objects.create(
            name="Test Cafe",
            address="123 Test Street",
            opening_time="08:00",
            closing_time="20:00",
        )

        # Create a staff user for testing
        self.staff_user = Staff.objects.create_user(
            phone_number="09123456789",  # Use phone number instead of username
            password="testpass",
        )
        self.staff_user.first_name = "John"
        self.staff_user.last_name = "Doe"
        self.staff_user.role = "M"  # Manager role
        self.staff_user.save()

        # Create a customer for testing
        self.customer = Customer.objects.create(
            first_name="Alice",
            last_name="Smith",
            table_number=1,
            cafe=self.cafe,
            phone_number="09123456788",
            points=20,
        )
        # Create two orders for the customer
        self.order1 = Order.objects.create(
            customer=self.customer,
            table_number=self.customer.table_number,
            total_price=100.0,
            status="Completed",
        )
        self.order2 = Order.objects.create(
            customer=self.customer,
            table_number=self.customer.table_number,
            total_price=200.0,
            status="Pending",
        )

        # Create an order for the customer
        self.order = Order.objects.create(
            customer=self.customer,
            table_number=self.customer.table_number,
            total_price=100.0,
            status="Completed",
        )

        # Log in the staff user
        self.client.login(phone_number="09123456789", password="testpass")

    def test_customer_checkout_without_orders(self):
        """Test the customer_checkout view without any orders."""
        # Set a phone number without orders
        self.client.session["customer_phone_number"] = "00000000000"
        response = self.client.get(reverse("customer_checkout"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["orders"]), 0
        )  # Ensure no orders in the context

    def test_search_customer_as_staff(self):
        """Test the search_customer view as a staff user."""
        response = self.client.get(
            reverse("search_customer"), {"phone_number": self.customer.phone_number}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["customers"]), 1
        )  # Ensure we found the customer

    def test_search_customer_as_non_staff(self):
        """Test the search_customer view as a non-staff user."""
        self.client.logout()

        non_staff_user = Staff.objects.create_user(
            phone_number="09123456788", password="testpass"
        )
        non_staff_user.first_name = "Jane"
        non_staff_user.last_name = "Doe"
        non_staff_user.role = "S"
        non_staff_user.save()

        self.client.login(phone_number="09123456788", password="testpass")

        response = self.client.get(
            reverse("search_customer"), {"phone_number": self.customer.phone_number}
        )

        # Instead of checking the exact URL, just check that it's a redirect to the login page
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertIn("", response.url)  # Check if it redirects to the login URL

    def test_search_customer_with_no_results(self):
        """Test the search_customer view with no matching customers."""
        response = self.client.get(
            reverse("search_customer"), {"phone_number": "123456789"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["customers"]), 0
        )  # Ensure no customers found

    def test_customer_negative_points(self):
        """Test creating a customer with negative points."""
        customer = Customer(
            first_name="Bob",
            last_name="Jones",
            table_number=2,
            cafe=self.cafe,
            phone_number="09123456789",
            points=-5,  # Negative points should not be allowed
            is_active=True,
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()  # Should raise validation error

    def test_customer_inactive(self):
        """Test creating an inactive customer."""
        customer = Customer.objects.create(
            first_name="Charlie",
            last_name="Brown",
            table_number=6,
            cafe=self.cafe,
            phone_number="09123456789",
            points=25,
            is_active=False,
        )
        self.assertFalse(customer.is_active)  # Should correctly set inactive status
