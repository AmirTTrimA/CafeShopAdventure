from django.contrib import admin
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for the Order model.

    This configuration allows the admin to view and manage customer orders.
    """
    
    list_display = ('id', 'customer', 'staff', 'status', 'total_price', 'order_date', 'created_at', 'updated_at')

    list_filter = ('status', 'order_date')

    search_fields = ('customer__first_name', 'customer__last_name', 'staff__first_name', 'staff__last_name')

    readonly_fields = ('total_price', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('customer', 'staff', 'status')
        }),
        ('Price Information', {
            'fields': ('total_price',)
        }),
        ('Timestamps', {
            'fields': ('order_date', 'created_at', 'updated_at'),
        }),
    )

    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        """
        Override save_model to calculate the total price before saving the order.
        """
        obj.calculate_total_price()
        super().save_model(request, obj, form, change)


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin interface for the OrderItem model.

    This configuration allows the admin to view and manage items in customer orders.
    """

    list_display = ('id', 'order', 'item', 'quantity', 'subtotal', 'created_at', 'updated_at')

    list_filter = ('order', 'item')

    search_fields = ('order__id', 'item__name')

    readonly_fields = ('subtotal', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('order', 'item', 'quantity')
        }),
        ('Subtotal Information', {
            'fields': ('subtotal',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        """
        Override save_model to calculate the subtotal before saving the order item.
        """
        obj.subtotal = obj.item.price * obj.quantity
        super().save_model(request, obj, form, change)


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin interface for the Cart model.

    This configuration allows the admin to view and manage customer carts.
    """

    list_display = ('id', 'customer', 'created_at')

    search_fields = ('customer__first_name', 'customer__last_name')

    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('customer',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Admin interface for the CartItem model.

    This configuration allows the admin to view and manage items in customer carts.
    """

    list_display = ('id', 'cart', 'menu_item', 'quantity')

    list_filter = ('cart', 'menu_item')

    search_fields = ('cart__id', 'menu_item__name')

    fieldsets = (
        (None, {
            'fields': ('cart', 'menu_item', 'quantity')
        }),
    )

    ordering = ('-cart__created_at',)
