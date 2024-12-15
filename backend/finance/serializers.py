from rest_framework import serializers
from .models import Income

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'name', 'amount', 'date_received', 'received_by', 'month', 'year']
        extra_kwargs = {
            'name': {'required': False, 'allow_null': True},
            'amount': {'required': False, 'allow_null': True},
            'date_received': {'required': False, 'allow_null': True},
            'received_by': {'required': False, 'allow_null': True},
            'month': {'required': False, 'allow_null': True},
            'year': {'required': False, 'allow_null': True},
        }
