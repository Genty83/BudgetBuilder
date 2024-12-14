from django.urls import path
from .views import FinanceManagerView

urlpatterns = [
    path('finance-manager/', FinanceManagerView.as_view(), name='finance-manager'),
]
