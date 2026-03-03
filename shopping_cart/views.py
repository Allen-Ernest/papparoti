import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from django.contrib import messages
from decimal import Decimal, ROUND_HALF_UP

from shopping_cart.cart import create_shopping_cart
from .models import Cart, CartItem
from menu.models import Menu

def get_cart_page(request):
    if request.user.is_authenticated and request.user.role == 'client':
        cart = Cart.objects.filter(user=request.user.client_profile, status='active').first()
        cart_items = CartItem.objects.filter(cart=cart) if cart else []
        #calculate total price
        price = sum(item.menu.price * item.quantity for item in cart_items)
        
        tax_rate = Decimal("0.07")
        estimated_tax = (Decimal(price) * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_price = (Decimal(price) + estimated_tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if not cart:
            return render(request, "empty_cart.html")
        return render(request, "cart.html", {'cart': cart, 'cart_items': cart_items, 'total_price': total_price, 'price': price, 'estimated_tax': estimated_tax})
    else:
        messages.error(request, 'Please log in to view your shopping cart.')
        return redirect("auth")
    
def get_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({"cart_items": []})

    cart = Cart.objects.filter(user=request.user.client_profile, status="active").first()

    if not cart:
        return JsonResponse({"cart_items": []})

    items = cart.cartitem_set.all()

    data = [
        {
            "menu_id": item.menu.id,
            "quantity": item.quantity
        }
        for item in items
    ]

    return JsonResponse({"cart_items": data})
    
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
        cart, _ = Cart.objects.get_or_create(user=client_profile, status='active')
        menu = Menu.objects.get(id=menu_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu=menu,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity = quantity   # overwrite quantity
            cart_item.save()

        cart_items_count = CartItem.objects.filter(cart=cart).count()

        return JsonResponse({
            'message': 'Cart updated successfully',
            'cart_items_count': cart_items_count,
            'menu_id': menu_id,
            'quantity': cart_item.quantity
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def view_cart(request):
    # This view will be used to view the contents of the shopping cart
    pass

def update_cart(request):
    # This view will be used to update the quantities of items in the shopping cart
    pass

@require_POST
def remove_from_cart(request):
    if not request.user.is_authenticated or request.user.role != 'client':
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    data = json.loads(request.body)
    menu_id = data.get('menu_id')

    client_profile = request.user.client_profile
    cart = Cart.objects.filter(user=client_profile, status='active').first()

    if cart:
        CartItem.objects.filter(cart=cart, menu_id=menu_id).delete()

    return JsonResponse({'message': 'Item removed'})

def checkout(request):
    pass

def delete_cart(request):
    # This view will be used to delete the shopping cart
    pass