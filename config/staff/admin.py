from django.contrib import admin
from . import models


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Staff members.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (tuple): Fields to filter the list view.
        search_fields (tuple): Fields to search within the list view.
        ordering (tuple): Default ordering of the list view.
        readonly_fields (tuple): Fields that are read-only in the admin form.
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
    ordering = ("last_name", "first_name")
    readonly_fields = ("staff_id",)  # Assuming staff_id should be read-only

    def has_change_permission(self, request, obj=None):
        """Override to restrict change permissions if needed."""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Override to restrict delete permissions if needed."""
        return request.user.is_superuser

    def get_queryset(self, request):
        """Customize the queryset to show only relevant staff members."""
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(is_staff=True)  
