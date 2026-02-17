from django.db import models

# Create your models here.
class Order(models.Model):
    client = models.ForeignKey('users.ClientProfile', on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu = models.ForeignKey('menu.Menu', on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField("Quantity", default=1)
    purchase_price = models.PositiveIntegerField("Purchase Price", default=0)

    def get_total_price(self):
        return self.quantity * self.purchase_price