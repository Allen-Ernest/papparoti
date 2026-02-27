from time import timezone

from .models import Cart

def create_shopping_cart(user):
    cart = Cart.objects.create(user=user, status='active', created_at=timezone.now(), updated_at=timezone.now())
    return cart