from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Order, OrderItem

def view_client_views(request, client_id):
    # This view will be used to view all orders of a specific client
    if request.user.is_authenticated and request.user.role == 'admin':
        orders = Order.objects.filter(client_id=client_id)
        return render(request, 'client_orders.html', {'orders': orders})
    else:
        messages.error(request, 'User not authenticated or not an admin')
        return redirect('auth', {'message': 'User not authenticated or not an admin'})
    
def view_order_items(request, order_id):
    # This view will be used to view all items of a specific order
    if request.user.is_authenticated and request.user.role == 'admin':
        order_items = OrderItem.objects.filter(order_id=order_id)
        return render(request, 'order_items.html', {'order_items': order_items})
    else:
        messages.error(request, 'User not authenticated or not an admin')
        return redirect('auth', {'message': 'User not authenticated or not an admin'})
    
def view_specific_order(request, order_id):
    # This view will be used to view a specific order with its items
    if request.user.is_authenticated and request.user.role == 'admin':
        try:
            order = Order.objects.get(id=order_id)
            order_items = OrderItem.objects.filter(order_id=order_id)
            return render(request, 'specific_order.html', {'order': order, 'order_items': order_items})
        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
            return redirect('view_client_views', client_id=order.client_id)
    else:
        messages.error(request, 'User not authenticated or not an admin')
        return redirect('auth', {'message': 'User not authenticated or not an admin'})
    
def update_order_status(request, order_id):
    # This view will be used to update the status of a specific order
    if request.method == "POST":
        if request.user.is_authenticated and request.user.role == 'admin':
            new_status = request.POST.get('status')
            if new_status in ['pending', 'completed', 'cancelled']:
                try:
                    order = Order.objects.get(id=order_id)
                    order.status = new_status
                    order.save()
                    messages.success(request, 'Order status updated successfully')
                except Order.DoesNotExist:
                    messages.error(request, 'Order not found')
            else:
                messages.error(request, 'Invalid status value')
        else:
            messages.error(request, 'User not authenticated or not an admin')
    else:
        messages.error(request, 'Bad request')
    return redirect('view_client_views', client_id=order.client_id)