from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline for displaying OrderItem within the Order admin."""

    model = OrderItem
    extra = 1
    readonly_fields = ("subtotal",)  # Make subtotal read-only in inline


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for managing Orders."""

    list_display = ("customer", "staff", "status", "order_date", "total_price")
    list_filter = ("status", "order_date")
    search_fields = (
        "customer__first_name",
        "customer__last_name",
        "staff__first_name",
        "staff__last_name",
    )
    inlines = [OrderItemInline]
    readonly_fields = ("total_price", "created_at", "updated_at")
    date_hierarchy = "order_date"
    ordering = ("-order_date",)  # Default ordering by order date descending


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for managing OrderItems."""

    list_display = ("order", "item", "quantity", "subtotal")
    search_fields = ("order__id", "item__name")
    readonly_fields = ("subtotal", "created_at", "updated_at")
    list_filter = ("order__status",)  # Filter by order status if needed
