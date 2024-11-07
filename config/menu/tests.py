from django.test import TestCase
from django.urls import reverse
from .models import MenuItem, Category
from datetime import timedelta
import time

class CafeMenuViewTests(TestCase):
    def setUp(self):
        """Create a category and some menu items for testing."""
        self.category = Category.objects.create(name='Beverages')
        MenuItem.objects.create(name='Coffee', price=2.5, category=self.category, is_available=True)
        MenuItem.objects.create(name='Tea', price=2.0, category=self.category, is_available=True)

    def test_cafe_menu_view_without_category(self):
        """Test the cafe menu view without a specific category."""
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertIn('menu_items', response.context)
        self.assertEqual(len(response.context['menu_items']), 2)  # Expecting two menu items
        self.assertEqual(len(response.context['cat_item']), 1)  # Ensure at least one category exists

    def test_cafe_menu_view_with_category(self):
        """Test the cafe menu view with a specific category."""
        response = self.client.get(reverse('menu_by_category', kwargs={'category_id': self.category.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertIn('menu_items', response.context)
        self.assertEqual(len(response.context['menu_items']), 2)  # Two items in this category
        self.assertEqual(response.context['cat_item'].first(), self.category)  # Ensure category is passed

class ProductDetailViewTests(TestCase):
    def setUp(self):
        """Create a category and a product for testing."""
        self.category = Category.objects.create(name='Beverages')
        self.product = MenuItem.objects.create(name='Coffee', price=2.5, category=self.category, is_available=True)

    def test_product_detail_view(self):
        """Test the product detail view."""
        response = self.client.get(reverse('product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')
        self.assertEqual(response.context['product'], self.product)  # Product should be in context

    def test_product_detail_view_not_found(self):
        """Test the product detail view with a non-existent product."""
        response = self.client.get(reverse('product', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Expecting a 404 response

class SearchViewTests(TestCase):
    def setUp(self):
        """Create a category and menu items for testing."""
        self.category = Category.objects.create(name='Beverages')
        MenuItem.objects.create(name='Coffee', price=2.5, category=self.category, is_available=True)
        MenuItem.objects.create(name='Tea', price=2.0, category=self.category, is_available=True)

    def test_search_view_with_results(self):
        """Test the search view with search results."""
        response = self.client.get(reverse('search'), {'q': 'Coffee'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertIn('menu_items', response.context)
        self.assertEqual(len(response.context['menu_items']), 1)  # Only one item should be present

    def test_search_view_without_results(self):
        """Test the search view without search results."""
        response = self.client.get(reverse('search'), {'q': 'Non-existent item'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertIn('menu_items', response.context)
        self.assertEqual(len(response.context['menu_items']), 0)  # No items should be present

    def test_search_view_case_insensitivity(self):
        """Test the search view is case insensitive."""
        response = self.client.get(reverse('search'), {'q': 'coffee'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['menu_items']), 1)  # Should still find the item

class CategoryModelTests(TestCase):
    def setUp(self):
        """Create a category instance for testing."""
        self.category = Category.objects.create(name='Beverages')

    def test_category_creation(self):
        """Test the category creation and string representation."""
        self.assertEqual(self.category.name, 'Beverages')
        self.assertIsNotNone(self.category.created_at)
        self.assertIsNotNone(self.category.updated_at)

    def test_str_method(self):
        """Test the string representation of the category."""
        self.assertEqual(str(self.category), 'Beverages')

    def test_update_timestamp(self):
        """Test the updated_at field is updated on save."""
        original_updated_at = self.category.updated_at

        # Change category name
        self.category.name = 'Updated Category'
        
        # Short delay to ensure time change
        time.sleep(0.1)  # 100 milliseconds

        self.category.save()  # Save the updated category

        # Reload from database
        self.category.refresh_from_db()

        # Ensure the updated_at timestamp has changed
        self.assertNotEqual(original_updated_at, self.category.updated_at)
        self.assertTrue(self.category.updated_at > original_updated_at + timedelta(seconds=0.1))

class MenuItemModelTests(TestCase):
    def setUp(self):
        """Create a category and a menu item instance for testing."""
        self.category = Category.objects.create(name='Beverages')
        self.menu_item = MenuItem.objects.create(
            name='Coffee',
            description='A hot drink made from roasted coffee beans.',
            price=2.50,
            points=10,
            category=self.category,
            is_available=True
        )

    def test_menu_item_creation(self):
        """Test the menu item creation and its fields."""
        self.assertEqual(self.menu_item.name, 'Coffee')
        self.assertEqual(self.menu_item.description, 'A hot drink made from roasted coffee beans.')
        self.assertEqual(self.menu_item.price, 2.50)
        self.assertEqual(self.menu_item.points, 10)
        self.assertEqual(self.menu_item.category, self.category)
        self.assertTrue(self.menu_item.is_available)
        self.assertIsNotNone(self.menu_item.created_at)
        self.assertIsNotNone(self.menu_item.updated_at)

    def test_str_method(self):
        """Test the string representation of the menu item."""
        self.assertEqual(str(self.menu_item), 'Coffee')

    def test_update_timestamp(self):
        """Test the updated_at field is updated on save."""
        original_updated_at = self.menu_item.updated_at

        # Change menu item name
        self.menu_item.name = 'Updated Coffee'
        
        # Short delay to ensure time change
        time.sleep(0.1)  # 100 milliseconds

        self.menu_item.save()  # Save the updated item

        # Reload from database
        self.menu_item.refresh_from_db()

        # Ensure the updated_at timestamp has changed
        self.assertNotEqual(original_updated_at, self.menu_item.updated_at)
        self.assertTrue(self.menu_item.updated_at > original_updated_at + timedelta(seconds=0.1))

    def test_menu_item_availability(self):
        """Test the availability status of the menu item."""
        self.menu_item.is_available = False
        self.menu_item.save()
        self.assertFalse(self.menu_item.is_available)

    def tearDown(self):
        """Clean up after tests."""
        self.menu_item.delete()
        self.category.delete()
