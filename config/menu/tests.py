from django.test import TestCase
from django.urls import reverse
from .models import MenuItem, Category
from datetime import timedelta
import time

class CafeMenuViewTests(TestCase):
    def setUp(self):
        # ایجاد یک دسته
        self.category = Category.objects.create(name='Beverages')
        # ایجاد چند مورد منو
        MenuItem.objects.create(name='Coffee', price=2.5, category=self.category, is_available=True)
        MenuItem.objects.create(name='Tea', price=2.0, category=self.category, is_available=True)

    def test_cafe_menu_view_without_category(self):
        """Test the cafe menu view without a specific category."""
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertIn('menu_items', response.context)  
        self.assertEqual(len(response.context['menu_items']), 2)  # انتظار دارید که دو مورد منو وجود داشته باشد
        self.assertEqual(len(response.context['cat_item']), 1)  # اطمینان حاصل کنید که حداقل یک دسته وجود دارد


    def test_cafe_menu_view_with_category(self):
        """Test the cafe menu view with a specific category."""
        response = self.client.get(reverse('menu_by_category', kwargs={'category_id': self.category.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertIn('menu_items', response.context)  
        self.assertEqual(len(response.context['menu_items']), 2)  # دو مورد در این دسته باید باشد
        self.assertEqual(response.context['cat_item'].first(), self.category)  # Ensure category is passed


class ProductDetailViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Beverages')
        self.product = MenuItem.objects.create(name='Coffee', price=2.5, category=self.category, is_available=True)

    def test_product_detail_view(self):
        """Test the product detail view."""
        response = self.client.get(reverse('product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')
        self.assertEqual(response.context['product'], self.product)  # محصول باید در context باشد

class SearchViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Beverages')
        MenuItem.objects.create(name='Coffee', price=2.5, category=self.category, is_available=True)
        MenuItem.objects.create(name='Tea', price=2.0, category=self.category, is_available=True)

    def test_search_view_with_results(self):
        """Test the search view with search results."""
        response = self.client.get(reverse('search'), {'q': 'Coffee'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertIn('menu_items', response.context)
        self.assertEqual(len(response.context['menu_items']), 1)  # فقط یک مورد باید باشد

    def test_search_view_without_results(self):
        """Test the search view without search results."""
        response = self.client.get(reverse('search'), {'q': 'Non-existent item'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertIn('menu_items', response.context)
        self.assertEqual(len(response.context['menu_items']), 0)  # هیچ موردی نباید باشد

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

        # تغییر نام دسته
        self.category.name = 'Updated Category'
        
        # تأخیر کوتاه برای اطمینان از تغییر زمان
        time.sleep(0.1)  # 100 میلی‌ثانیه

        self.category.save()  # Save the updated category

        # دوباره بارگذاری از پایگاه داده
        self.category.refresh_from_db()

        # اطمینان از اینکه تاریخ زمان به روز رسانی تغییر کرده است
        self.assertNotEqual(original_updated_at, self.category.updated_at)

        # بررسی اینکه updated_at به زمان حال نزدیک است
        self.assertTrue(self.category.updated_at > original_updated_at + timedelta(seconds=0.1))  # اطمینان از اینکه حداقل 100 میلی‌ثانیه به روز شده استاطمینان از اینکه حداقل یک ثانیه به روز شده استpdated_at باید بزرگتر از original_updated_at باشد

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

        # تغییر نام مورد منو
        self.menu_item.name = 'Updated Coffee'
        
        # تأخیر کوتاه برای اطمینان از تغییر زمان
        time.sleep(0.1)  # 100 میلی‌ثانیه

        self.menu_item.save()  # Save the updated item

        # دوباره بارگذاری از پایگاه داده
        self.menu_item.refresh_from_db()

        # اطمینان از اینکه تاریخ زمان به روز رسانی تغییر کرده است
        self.assertNotEqual(original_updated_at, self.menu_item.updated_at)

        # بررسی اینکه updated_at به زمان حال نزدیک است
        self.assertTrue(self.menu_item.updated_at > original_updated_at + timedelta(seconds=0.1))  # اطمینان از اینکه حداقل 100 میلی‌ثانیه به روز شده است  # اطمینان از اینکه حداقل یک ثانیه به روز شده است