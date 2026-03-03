from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from ..models import Order, OrderItem

def get_order_manager(request):
    if not (request.user.is_authenticated and request.user.role == 'admin'):
        messages.error(request, "Unauthorized")
        return redirect('auth_admin')

    filter_status = request.GET.get('status')

    orders = Order.objects.all().order_by('-created_at')

    if filter_status and filter_status != "all":
        orders = orders.filter(status=filter_status)

    today = timezone.now().date()

    total_orders_today = Order.objects.filter(created_at__date=today).count()
    pending_count = Order.objects.filter(status='pending').count()
    processing_count = Order.objects.filter(status='processing').count()
    completed_count = Order.objects.filter(status='completed').count()

    revenue = Order.objects.aggregate(
        total=Sum('total_price')
    )['total'] or 0

    context = {
        'orders': orders,
        'pending_count': pending_count,
        'processing_count': processing_count,
        'completed_count': completed_count,
        'revenue': revenue,
        'total_orders_today': total_orders_today,
        'current_filter': filter_status or "all"
    }
    
    return render(request, 'order_manager.html', context)
    
def complete_order(request, order_id):
    if not (request.user.is_authenticated and request.user.role == 'admin'):
        messages.error(request, "Unauthorized")
        return redirect('auth_admin')

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.status = "completed"
        order.save()
        messages.success(request, f"Order {order.order_number} marked as completed.")
        return redirect('order_manager')

    return redirect('order_manager')

def update_order_status(request, order_id, new_status):
    if not (request.user.is_authenticated and request.user.role == 'admin'):
        return redirect('auth_admin')

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.status = new_status
        order.save()

    return redirect('order_manager')

def view_client_orders(request, client_id):
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