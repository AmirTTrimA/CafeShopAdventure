from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from . import models

User = get_user_model()  # Get the custom user model


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for the Customer model.
    """

    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "table_number",
        "cafe",
        "points",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = ("is_active",)

    search_fields = ("first_name", "last_name", "phone_number","table_number","cafe", "gender","date_of_birth",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "table_number",
                    "cafe",
                    "points",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to ensure a user is created.
        """
        if not obj.id:  # If user is not set
            # Create a User instance if it doesn't exist
            user = User.objects.create_user(
                phone_number=obj.phone_number,  # Assuming phone_number is used for user creation
                password="defaultpassword",  # Set a default password or generate one
            )
            obj.user = user  # Assign the user to the customer
        super().save_model(request, obj, form, change)
