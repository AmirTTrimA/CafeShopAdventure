from django.contrib import admin
from . import models

@admin.register(models.Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'opening_time', 'closing_time', 'created_at')
    search_fields = ('name', 'owner__username', 'address')
