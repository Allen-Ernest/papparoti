import json
from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.db import transaction

from shopping_cart.models import Cart, CartItem
from transaction.models import Transaction
from .models import Order, OrderItem


@require_POST
@transaction.atomic
def process_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    if request.user.role != 'client':
        return JsonResponse({"status": "ERROR", "message": "Unauthorized"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "ERROR", "message": "Invalid JSON"}, status=400)

    address = data.get("address", {})
    payment = data.get("payment", {})

    if not address or not payment:
        return JsonResponse({"status": "ERROR", "message": "Invalid request"}, status=400)

    # Extract address
    full_name = address.get("full_name")
    phone = address.get("phone")
    street_address = address.get("street_address")
    city = address.get("city")
    postal_code = address.get("postal_code")

    if not all([full_name, phone, street_address, city, postal_code]):
        return JsonResponse(
            {"status": "ERROR", "message": "Address data incomplete"},
            status=400
        )

    card_num = payment.get("card_number")
    expiry_date = payment.get("expiry")
    cvv = payment.get("cvv")

    if not all([card_num, expiry_date, cvv]):
        return JsonResponse(
            {"status": "ERROR", "message": "Payment info incomplete"},
            status=400
        )

    cart = Cart.objects.filter(
        user=request.user.client_profile,
        status='active'
    ).first()

    if not cart:
        return JsonResponse({'error': 'No active cart found'}, status=400)

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    subtotal = sum(item.menu.price * item.quantity for item in cart_items)

    tax_rate = Decimal("0.07")
    vat = (Decimal(subtotal) * tax_rate).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    total_price = (Decimal(subtotal) + vat).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    order = Order.objects.create(
        client=request.user.client_profile,
        full_name=full_name,
        phone=phone,
        street_address=street_address,
        city=city,
        postal_code=postal_code,
        total_price=total_price
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            menu=item.menu,
            quantity=item.quantity,
            purchase_price=item.menu.price
        )

    Transaction.objects.create(
        order=order,
        amount=total_price,
        transaction_date=timezone.now(),
        status="Completed"
    )

    cart.status = 'ordered'
    cart.save() 

    return JsonResponse({
        "success": True,
        "message": "Order processed successfully",
        "order_number": order.order_number,
        "order": order.id,
    }, status=200)

def get_checkout_page(request):
    if request.user.is_authenticated and request.user.role == 'client':
        if not Cart.objects.filter(user=request.user.client_profile, status='active').exists():
            messages.error(request, 'Your cart is empty. Please add items to your cart before checking out.')
            return redirect('cart')
        cart = Cart.objects.filter(user=request.user.client_profile, status='active').first()
        cart_items = CartItem.objects.filter(cart=cart) if cart else []
        price = sum(item.menu.price * item.quantity for item in cart_items)
        tax_rate = Decimal("0.07")
        vat = (Decimal(price) * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_price = (Decimal(price) + vat).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        full_name = f"{request.user.first_name} {request.user.last_name}"
        phone = request.user.client_profile.phone
        return render(request, "checkout.html", {'cart_items': cart_items, 'price': price, 'vat': vat, 'total_price': total_price, 'full_name': full_name, 'phone': phone})
    else:
        messages.error(request, 'Unauthorized access.')
        return redirect("auth")
    
def get_orders_page(request):
    orders = Order.objects.filter(
        client=request.user.client_profile
    ).order_by('-created_at')

    now = timezone.now()

    for order in orders:
        if order.status == 'pending':
            expiry_time = order.created_at + timedelta(hours=1)

            if now >= expiry_time:
                order.status = 'completed'
                order.save()
                order.remaining_seconds = 0
            else:
                remaining = (expiry_time - now).total_seconds()
                order.remaining_seconds = int(remaining)
        else:
            order.remaining_seconds = 0

    return render(request, "orders.html", {
        "orders": orders,
        "now": now
    })
    
def place_order(request):
    if (request.method == "POST"):
        user = request.user
        if user.is_authenticated and user.role == 'client':
            order = Order.objects.create(client=user.clientprofile, created_at=timezone.now())
            order_items_data = request.POST.getlist('order_items')
            for item_data in order_items_data:
                menu_id, quantity, purchase_price = item_data.split(',')
                OrderItem.objects.create(order=order, menu_id=menu_id, quantity=quantity, purchase_price=purchase_price)
            return render(request, 'order_success.html', {'order': order}) #TODO: create order success page to view and cancel order
        else:
            messages.error(request, 'User not authenticated or not a client')
            return redirect('auth', {'message': 'User not authenticated or not a client'})
    else:
        messages.error(request, 'Bad request')
        return redirect('home', {'message': 'Bad request'})

def view_orders(request):
    if request.user.is_authenticated and request.user.role == 'client':
        orders = Order.objects.filter(client=request.user.clientprofile)
        return render(request, 'view_orders.html', {'orders': orders})
    else:
        messages.error(request, 'User not authenticated or not a client')
        return redirect('auth', {'message': 'User not authenticated or not a client'})
    
def cancel_order(request, order_id):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated and user.role == 'client':
            try:
                order = Order.objects.get(id=order_id, client=user.clientprofile)
                if order.status == 'pending':
                    order.status = 'cancelled'
                    order.save()
                    messages.success(request, 'Order cancelled successfully')
                else:
                    messages.error(request, 'Only pending orders can be cancelled')
            except Order.DoesNotExist:
                messages.error(request, 'Order not found')
        else:
            messages.error(request, 'User not authenticated or not a client')
    else:
        messages.error(request, 'Bad request')
    return redirect('view_orders')