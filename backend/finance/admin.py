from django.contrib import admin
from .models import Income

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Income model.
    
    Fields:
        list_display: A tuple containing the fields to be displayed in the list view.
        search_fields: A tuple containing the fields on which to perform searches.
    """
    list_display = ('name', 'amount', 'date_received', 'received_by', 'month', 'year')
    search_fields = ('name', 'received_by', 'month', 'year')
