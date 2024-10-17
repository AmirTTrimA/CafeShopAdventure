from django.contrib import admin
from . import models


@admin.register(models.SalesAnalytics)
class SalesAnalyticsAdmin(admin.ModelAdmin):
    """
    Admin interface for the SalesAnalytics model.

    This configuration allows the admin to view and manage sales analytics.
    """

    list_display = ('date', 'staff', 'total_sales', 'total_orders', 'created_at', 'updated_at')

    list_filter = ('date', 'staff')

    search_fields = ('staff__name', 'date')

    readonly_fields = ('total_sales', 'total_orders', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('date', 'staff', 'total_sales', 'total_orders')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to calculate totals before saving.
        This ensures that totals are recalculated when saving from the admin.
        """
        obj.calculate_totals()
        super().save_model(request, obj, form, change)
