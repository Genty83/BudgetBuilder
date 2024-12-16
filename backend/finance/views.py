from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from .models import Income
from .serializers import IncomeSerializer

class FinanceManagerView(TemplateView):
    template_name = 'finance_manager.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Welcome to Finance Manager!'
        return context

class IncomeCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'created'  # Or any other field for ordering

class IncomeListView(APIView):
    def get(self, request):
        incomes = Income.objects.all()
        paginator = IncomeCursorPagination()
        result_page = paginator.paginate_queryset(incomes, request)
        serializer = IncomeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
