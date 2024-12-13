from django.db import models

class Income(models.Model):
    """
    Represents an income entry with details such as name, amount,
    date received, the person who received it, the month, and the year.
    
    Attributes:
        name (str): The name or source of the income.
        amount (Decimal): The amount of income received.
        date_received (Date): The date the income was received.
        received_by (str): The person who received the income.
        month (str): The month when the income was received.
        year (int): The year when the income was received.
    """

    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    received_by = models.CharField(max_length=100)
    month = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        """
        Returns a string representation of the Income instance.

        Returns:
            str: A string describing the income details.
        """
        return f"{self.name} - {self.amount} received on {self.date_received}"
