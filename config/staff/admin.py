from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "role", "created_at")
    list_filter = ("role",)
    search_fields = ("first_name", "last_name", "email")
    readonly_fields = ("created_at", "updated_at")
