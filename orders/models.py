from django.db import models

# Create your models here.
class Order(models.Model):
    client = models.ForeignKey('users.ClientProfile', on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending') #could be pending, completed, cancelled
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    total_price = models.PositiveIntegerField("Total Price", default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu = models.ForeignKey('menu.Menu', on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField("Quantity", default=1)
    purchase_price = models.PositiveIntegerField("Purchase Price", default=0)

    def get_total_price(self):
        return self.quantity * self.purchase_price
    
    #TODO: add a method to calculate the total price of the order based on the order items
    #TODO: implement shopping cart and placing order