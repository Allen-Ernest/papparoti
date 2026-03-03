from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.get_cart_page, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('get-cart/', views.get_cart, name='get_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
]