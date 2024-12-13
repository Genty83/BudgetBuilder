from django.views.generic import ListView
from .models import Income

class IncomeListView(ListView):
    """
    Displays a list of income entries.
    
    Attributes:
        model: The model to be used (Income).
        template_name: The path to the template file to be rendered.
        context_object_name: The name of the context variable to be used in the template.
    """
    model = Income
    template_name = 'finance-manager.html'
    context_object_name = 'incomes'
