from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Order, OrderItem

def get_order_manager(request):
    if request.user.is_authenticated and request.user.role == 'admin':
        orders = Order.objects.all()
        return render(request, 'order_manager.html', {'orders': orders})
    else:
        messages.error(request, 'User not authenticated or not an admin')
        return redirect('auth', {'message': 'User not authenticated or not an admin'})
    
def create_order(request):
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