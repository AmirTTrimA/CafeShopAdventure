"""
This module contains the data models for the Cafe application.

It defines the following models:
- Cafe: Represents a cafe with attributes such as name, address, owner, opening and closing times, and the number of tables.
- Table: Represents a table within a cafe, including its number, status, and the cafe it belongs to.
"""

from django.db import models


class Cafe(models.Model):
    """
    Represents a Cafe in the system.

    Attributes:
        name (str): The name of the cafe.
        address (str): The address of the cafe.
        owner (ForeignKey): The owner (User) of the cafe.
        opening_time (TimeField): The time the cafe opens.
        closing_time (TimeField): The time the cafe closes.

    """

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    # owner = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # number_of_tables = models.PositiveIntegerField(default=1)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def is_open(self, current_time):
        """
        Check if the cafe is open based on the current time.
        """
        return self.opening_time <= current_time <= self.closing_time


class Table(models.Model):
    """
    Represents a Table in a Cafe.

    Attributes:
        cafe (ForeignKey): The cafe to which the table belongs.
        number (int): The table number.
        status (str): The current status of the table (available or unavailable).
        created_at (DateTime): The timestamp when the table was created.
    """

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("A", "available"),
            ("U", "unavailable"),
        ],
        default="available",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the Table.

        Returns:
                str: A string with the format "Table <number> in <cafe name>".
        """
        return f"Table {self.number} in {self.cafe.name}"

    def is_available(self):
        """
        Check if the table is available.

        Returns:
            bool: True if the table status is "available", False otherwise.
        """
        return self.status == "available"

    def which_number(self):
        """
        Return the table number.

        Returns:
            int: The table number.
        """
        return self.number
