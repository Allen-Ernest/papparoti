import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from django.contrib import messages

from shopping_cart.cart import create_shopping_cart
from .models import Cart, CartItem
from menu.models import Menu

def get_cart_page(request):
    if request.user.is_authenticated:
        return render(request, "cart.html")
    else:
        messages.error(request, 'Please log in to view your shopping cart.')
        return redirect("auth")

@require_POST
def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    try:
        data = json.loads(request.body)
        menu_id = data.get('menu_id')
        quantity = int(data.get('quantity', 1))
        
        if not menu_id or quantity < 1:
            return JsonResponse({'error': 'Invalid menu ID or quantity'}, status=400)
        
        client_profile = request.user.client_profile
        cart, created = Cart.objects.get_or_create(user=client_profile, status='active')
        menu = Menu.objects.get(id=menu_id)
        CartItem.objects.create(cart=cart, menu=menu, quantity=quantity)
        #return number of cart items in the cart
        cart_items_count = CartItem.objects.filter(cart=cart).count()
        return JsonResponse({'message': 'Item added to cart successfully', 'cart_items_count': cart_items_count})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def view_cart(request):
    # This view will be used to view the contents of the shopping cart
    pass

def update_cart(request):
    # This view will be used to update the quantities of items in the shopping cart
    pass

def remove_from_cart(request):
    # This view will be used to remove items from the shopping cart
    pass

def checkout(request):
    pass

def delete_cart(request):
    # This view will be used to delete the shopping cart
    pass