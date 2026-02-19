from django.shortcuts import render
from ..models import Cart

def see_all_carts(request):
    carts = Cart.objects.all()
    return render(request, 'cart_management/all_carts.html', {'carts': carts})

def see_cart_items(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
        cart_items = cart.cartitem_set.all()
        return render(request, 'cart_management/cart_items.html', {'cart': cart, 'cart_items': cart_items})
    except Cart.DoesNotExist:
        return render(request, 'cart_management/cart_items.html', {'error': 'Cart not found'})