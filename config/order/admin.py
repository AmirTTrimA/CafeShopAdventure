"""admin.py

This module registers the admin interfaces for the Order and related models,
allowing the management of customer orders, order items, and order history.
"""

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin interface for displaying order items within an order."""

    model = OrderItem
    extra = 1  # Number of empty forms to display


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for the Order model.

    This configuration allows the admin to view and manage customer orders.
    """

    inlines = [OrderItemInline]
    list_display = (
        "id",
        "customer",
        "staff",
        "status",
        "total_price",
        "order_date",
        "created_at",
        "updated_at",
    )

    list_filter = ("status", "order_date")

    search_fields = (
        "customer__first_name",
        "customer__last_name",
        "staff__first_name",
        "staff__last_name",
    )

    readonly_fields = ("total_price", "created_at", "updated_at", "order_date")

    fieldsets = (
        (None, {"fields": ("customer", "staff", "status")}),
        ("Price Information", {"fields": ("total_price",)}),
        (
            "Timestamps",
            {
                "fields": ("order_date", "created_at", "updated_at"),
            },
        ),
    )

    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin interface for the OrderItem model.

    This configuration allows the admin to view and manage items in customer orders.
    """

    list_display = (
        "id",
        "order",
        "item",
        "quantity",
        "subtotal",
        "created_at",
        "updated_at",
    )

    list_filter = ("order", "item")

    search_fields = ("order__id", "item__name")

    readonly_fields = ("subtotal", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("order", "item", "quantity")}),
        ("Subtotal Information", {"fields": ("subtotal",)}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
