from django.urls import path
from . import views

urlpatterns = [
    path('order_manager/', views.get_order_manager, name='order_manager'),
]