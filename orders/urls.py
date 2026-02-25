from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.get_orders_page, name='orders'),
    path('order_manager/', views.get_order_manager, name='order_manager'),
]