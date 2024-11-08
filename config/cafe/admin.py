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

    list_display = ("name", "address", "opening_time", "closing_time", "created_at")
    search_fields = (
        "name",
        "address",
    )


@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Table instances in the Django admin site.
    - Displaying important fields in the list view:
      - Number of the table
      - Status of the table
      - Name of the cafe
      - Creation timestamp
    - Enabling search functionality on the following fields:
      - Number
    """

    list_display = ("number", "status", "cafe", "created_at")
    search_fields = ("number",)
