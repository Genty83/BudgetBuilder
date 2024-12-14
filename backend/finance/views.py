from django.views.generic import TemplateView
from django.core.paginator import Paginator
from .models import Income

class FinanceManagerView(TemplateView):
    template_name = 'finance/finance_manager.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        income_list = Income.objects.all()
        paginator = Paginator(income_list, 10)  # Show 10 incomes per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        context['start_index'] = page_obj.start_index()  # Start index of records
        context['end_index'] = page_obj.end_index()      # End index of records
        context['total_count'] = paginator.count         # Total number of records
        context['headers'] = ['Name', 'Amount', 'Date Received', 'Received By', 'Month', 'Year']
        
        return context
