from django.urls import path
from .views import IncomeListView, FinanceManagerView

urlpatterns = [
    path('', FinanceManagerView.as_view(), name='finance-manager'),
    path('api/incomes/', IncomeListView.as_view(), name='income-list'),
    path('api/incomes/<int:pk>/', IncomeListView.as_view(), name='income-detail'),  # URL pattern for delete and detail
]
