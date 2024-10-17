from django.contrib import admin
from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for the Customer model.

    This configuration allows the admin to view and manage customer details.
    """

    list_display = ('first_name', 'last_name', 'phone_number', 'points', 'is_active', 'created_at', 'updated_at')

    list_filter = ('is_active',)

    search_fields = ('first_name', 'last_name', 'phone_number')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'phone_number', 'points', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method if needed.
        """
        super().save_model(request, obj, form, change)
