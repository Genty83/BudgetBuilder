from django.db import models

class Income(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)        
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  
    date_received = models.DateField(blank=True, null=True)              
    received_by = models.CharField(max_length=100, blank=True, null=True) 
    month = models.CharField(max_length=20, blank=True, null=True)  # Change month to CharField
    year = models.IntegerField(blank=True, null=True)                    

    def __str__(self):
        return self.name if self.name else 'Income Entry'

    class Meta:
        ordering = ['id']  # Order by 'id'
