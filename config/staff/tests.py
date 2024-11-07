from django.test import TestCase
from .models import Staff
from django.core.exceptions import ValidationError
from django.urls import reverse

class StaffModelTests(TestCase):

    def setUp(self):
        """Create a staff member for testing."""
        self.staff = Staff.objects.create_user(
            phone_number="09123456789",
            password="testpassword"
        )
        self.staff.first_name = "John"
        self.staff.last_name = "Doe"
        self.staff.save()

    def test_staff_creation(self):
        """Test if the staff member is created correctly."""
        self.assertEqual(self.staff.first_name, "John")
        self.assertEqual(self.staff.last_name, "Doe")
        self.assertEqual(self.staff.phone_number, "09123456789")
        self.assertEqual(self.staff.role, "S")
        self.assertTrue(self.staff.check_password("testpassword"))
        self.assertTrue(self.staff.is_active)

    def test_staff_manager_creation(self):
        """Test if the staff manager is created correctly."""
        manager = Staff.objects.create_superuser(
            phone_number="09876543210",
            password="superpassword"
        )
        self.assertTrue(manager.is_superuser)
        self.assertEqual(manager.role, "M")

    def test_phone_number_unique(self):
        # تلاش برای ایجاد یک Staff جدید با شماره تلفن تکراری
        with self.assertRaises(Exception):  # یا استفاده از specific exception like IntegrityError
            Staff.objects.create(phone_number=self.staff_member.phone_number)
    def test_set_password_hashing(self):
        """Test that the password is hashed when set."""
        staff = Staff.objects.create_user(
            phone_number="01234567890",
            password="mypassword"
        )
        self.assertNotEqual(staff.password, "mypassword")  # Ensure password is hashed
        self.assertTrue(staff.check_password("mypassword"))  # Check hashed password

    def test_is_staff_property(self):
        """Test the is_staff property."""
        self.assertFalse(self.staff.is_staff)  # Should be False for regular staff
        manager = Staff.objects.create_superuser(
            phone_number="12345678901",
            password="managerpassword"
        )
        self.assertTrue(manager.is_staff)  # Should be True for manager


    def test_staff_invalid_role(self):
        """Test creating a staff member with an invalid role."""
        staff = Staff(
            phone_number='09123456788',
            password='testpass',
            first_name='Invalid',
            last_name='Role',
            role='InvalidRole'  # Invalid role
        )
        with self.assertRaises(ValidationError):
            staff.full_clean()  # Should raise validation error

    # def test_staff_login(self):
    #     """Test that staff member can log in."""
    #     self.client.login(phone_number='09123456789', password='testpass')
    #     response = self.client.get(reverse('staff_dashboard'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'staff_dashboard.html')  # Assuming the staff dashboard template


    def test_search_customer_no_phone(self):
        """Test the search_customer view with no phone number provided."""
        response = self.client.get(reverse('search_customer'), {'phone_number': ''})       
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)  
