from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.

    This configuration allows the admin to view and manage menu categories.
    """

    list_display = ("name", "created_at", "updated_at")

    list_filter = ("created_at",)

    search_fields = ("name",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("name",)}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Admin interface for the MenuItem model.

    This configuration allows the admin to view and manage menu items.
    """

    list_display = (
        "name",
        "category",
        "price",
        "points",
        "is_available",
        "created_at",
        "updated_at",
    )

    list_filter = ("is_available", "category", "created_at")

    search_fields = ("name", "description")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "price",
                    "points",
                    "category",
                    "is_available",
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

    ordering = ("-created_at",)
