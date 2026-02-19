from django.db import models

class Cart(models.Model):
    user = models.ForeignKey('users.ClientProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='active') # could be active, checked_out, cancelled

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)