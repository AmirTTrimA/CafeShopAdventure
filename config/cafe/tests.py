from django.test import TestCase, Client
from django.urls import reverse
from menu.models import MenuItem, Category
from .models import Cafe
from datetime import time
from django.core.exceptions import ValidationError

class MyViewTests(TestCase):
    def setUp(self):
        # Create a test client for making requests
        self.client = Client()
        # Create a category for menu items
        self.category = Category.objects.create(name='Category 1')
        # Create available and unavailable menu items in the category
        self.menu_item1 = MenuItem.objects.create(name='Item 1', price=10.0, category=self.category, is_available=True)
        self.menu_item2 = MenuItem.objects.create(name='Item 2', price=15.0, category=self.category, is_available=False)

    def test_my_view_get(self):
        """Test the GET request for the home view."""
        response = self.client.get(reverse('home'))
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'index.html')
        # Assert that the available menu item is included in the context
        self.assertIn(self.menu_item1, response.context['menu_items'])
        # Assert that the unavailable menu item is not included in the context
        self.assertNotIn(self.menu_item2, response.context['menu_items'])
        # Assert that the category is included in the context
        self.assertIn(self.category, response.context['cat_item'])

class ContactViewTests(TestCase):
    def test_contact_view_get(self):
        """Test the GET request for the contact view."""
        response = self.client.get(reverse('contact'))
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'contact.html')

class AboutViewTests(TestCase):
    def test_about_view_get(self):
        """Test the GET request for the about view."""
        response = self.client.get(reverse('about'))
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'about.html')

class CafeModelTests(TestCase):
    def setUp(self):
        # Create a test Cafe instance with predefined attributes
        self.cafe = Cafe.objects.create(
            name='Test Cafe',
            address='123 Test Street',
            number_of_tables=5,
            opening_time=time(8, 0),  # Use datetime.time for opening time
            closing_time=time(20, 0),  # Use datetime.time for closing time
        )

    def test_cafe_creation(self):
        """Test the creation of Cafe with proper attributes."""
        # Assert that the cafe name is correctly set
        self.assertEqual(self.cafe.name, 'Test Cafe')
        # Assert that the cafe address is correctly set
        self.assertEqual(self.cafe.address, '123 Test Street')
        # Assert that the number of tables is correctly set
        self.assertEqual(self.cafe.number_of_tables, 5)
        # Assert that the opening time is correctly set
        self.assertEqual(self.cafe.opening_time, time(8, 0))  # Compare with datetime.time
        # Assert that the closing time is correctly set
        self.assertEqual(self.cafe.closing_time, time(20, 0))  # Compare with datetime.time

    def test_is_open(self):
        """Test the is_open method to check if the cafe is open at a given time."""
        open_time = time(9, 0)  # Define the time to check if the cafe is open
        # Assert that the cafe is open at the specified time
        self.assertTrue(self.cafe.is_open(open_time), "Cafe should be open at 09:00")

    def test_cafe_invalid_opening_time(self):
        """Test creating a cafe with invalid opening and closing times."""
        cafe = Cafe(
            name='Invalid Cafe',
            address='123 Test Street',
            number_of_tables=10,
            opening_time='25:00',  # Invalid time
            closing_time='20:00'
        )
        with self.assertRaises(ValidationError):
            cafe.full_clean()  # Should raise validation error

    def test_cafe_name_empty(self):
        """Test creating a cafe with an empty name."""
        cafe = Cafe(
            name='',
            address='123 Test Street',
            number_of_tables=10,
            opening_time='08:00',
            closing_time='20:00',
        )
        with self.assertRaises(ValidationError):
            cafe.full_clean()  # Should raise validation error

