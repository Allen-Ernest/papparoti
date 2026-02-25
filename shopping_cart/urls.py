from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.get_cart_page, name='cart'),
    path('create_cart/', views.create_shopping_cart, name='create_cart'),
]