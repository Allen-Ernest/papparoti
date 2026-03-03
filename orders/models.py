from django.db import models
import random

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
    order_number = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    def generate_order_number(self):
        return f"PR-{random.randint(1000, 9999)}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            new_number = self.generate_order_number()

            while Order.objects.filter(order_number=new_number).exists():
                new_number = self.generate_order_number()

            self.order_number = new_number

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu = models.ForeignKey('menu.Menu', on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField("Quantity", default=1)
    purchase_price = models.PositiveIntegerField("Purchase Price", default=0)

    def get_total_price(self):
        return self.quantity * self.purchase_price