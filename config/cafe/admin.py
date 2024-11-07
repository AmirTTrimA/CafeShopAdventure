from django.contrib import admin
from . import models

@admin.register(models.Cafe)
class CafeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Cafe instances in the Django admin site.
    - Displaying important fields in the list view:
      - Name of the cafe
      - Address of the cafe
      - Number of tables available
      - Opening time
      - Closing time
      - Creation timestamp

    - Enabling search functionality on the following fields:
      - Name
      - Address
      - Number of tables
    """
    list_display = ('name', 'address','number_of_tables', 'opening_time', 'closing_time', 'created_at')
    search_fields = ('name', 'address','number_of_tables',)
