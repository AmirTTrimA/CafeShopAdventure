from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Staff members.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (tuple): Fields to filter the list view.
        search_fields (tuple): Fields to search within the list view.
    """

    list_display = (
        "staff_id",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_staff",
        "is_superuser",
    )

    list_filter = ("role", "is_staff", "is_superuser")
    search_fields = ("first_name", "last_name", "email")

    def has_change_permission(self, request, obj=None):
        """Override to restrict change permissions if needed."""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Override to restrict delete permissions if needed."""
        return request.user.is_superuser
