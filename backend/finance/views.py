from django.views.generic import TemplateView
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import messages
from .models import Income
from .serializers import IncomeSerializer


class FinanceManagerView(TemplateView):
    """View for the finance manager page."""

    template_name = 'finance/finance_manager.html'

    def get_context_data(self, **kwargs):
        """
        Get context data for the template.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        return context


class IncomeListView(APIView):
    """API view for handling income data."""

    def get(self, request, format=None):
        """
        Handle GET requests for income data.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing paginated income data.
        """
        page = request.GET.get('page', 1)
        rows_per_page = int(request.GET.get('rows_per_page', 10))

        incomes = Income.objects.all().order_by('id')
        paginator = Paginator(incomes, rows_per_page)
        page_obj = paginator.get_page(page)

        serializer = IncomeSerializer(page_obj.object_list, many=True)
        data = {
            "headers": [
                'ID', 'Name', 'Amount', 'Date Received', 'Received By',
                'Month', 'Year'
            ],
            "incomes": serializer.data,
            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "has_previous": page_obj.has_previous(),
                "has_next": page_obj.has_next(),
                "previous_page_number": page_obj.previous_page_number() 
                                        if page_obj.has_previous() else None,
                "next_page_number": page_obj.next_page_number()
                                    if page_obj.has_next() else None,
                "total_records": paginator.count,
            }
        }
        return Response(data)

    def post(self, request, format=None):
        """
        Handle POST requests to create a new income entry.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response with the created income data or errors.
        """
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        messages.error(request, 'Failed to create income entry.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """
        Handle PUT requests to update an existing income entry.

        Args:
            request (HttpRequest): The request object.
            pk (int): The primary key of the income entry to update.

        Returns:
            Response: The response with the updated income data or errors.
        """
        try:
            income = Income.objects.get(pk=pk)
        except Income.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IncomeSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Handle DELETE requests to delete an income entry.

        Args:
            request (HttpRequest): The request object.
            pk (int): The primary key of the income entry to delete.

        Returns:
            Response: The response with the status of the deletion.
        """
        try:
            income = Income.objects.get(pk=pk)
            income.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Income.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
