from django.contrib import admin
from .models import Category, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')  
    search_fields = ('name',)  
    readonly_fields = ('created_at', 'updated_at')  

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'created_at')  
    list_filter = ('category', 'is_available')  
    search_fields = ('name', 'category__name')  
    readonly_fields = ('created_at', 'updated_at')  

