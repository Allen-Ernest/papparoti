from django.db import models

class Transaction(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField("Amount", default=0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending') #could be pending, completed, failed
