from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
    
def get_success_page(request, order_id):
    order = Order.objects.get(pk=order_id)
    delivery_time = timezone.now() + timedelta(hours=1)
    estimated_time = delivery_time.strftime("%H:%M")
    return render(request, "order_success.html", {"order": order, "delivery_time": estimated_time})

def get_error_page(request):
    return render(request, "order_failed.html")