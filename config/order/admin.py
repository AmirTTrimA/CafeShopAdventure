from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1   

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'staff', 'status', 'order_date', 'total_price')  
    list_filter = ('status', 'order_date')  
    search_fields = ('customer__first_name', 'customer__last_name', 'staff__first_name', 'staff__last_name')  
    inlines = [OrderItemInline]  
    readonly_fields = ('total_price', 'created_at', 'updated_at')  
    date_hierarchy = 'order_date'  

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'subtotal')  
    search_fields = ('order__id', 'item__name')  
    readonly_fields = ('subtotal', 'created_at', 'updated_at')  

