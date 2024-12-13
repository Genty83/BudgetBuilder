from django.urls import path
from .views import IncomeListView

urlpatterns = [
    path('incomes/', IncomeListView.as_view(), name='income-list'),
]
