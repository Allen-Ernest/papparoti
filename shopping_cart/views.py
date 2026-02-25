from pyexpat.errors import messages

from django.shortcuts import redirect, render
from django.contrib import messages

def get_cart_page(request):
    if request.user.is_authenticated:
        return render(request, "cart.html")
    else:
        messages.error(request, 'Please log in to view your shopping cart.')
        return redirect("auth")

def create_shopping_cart(request):
    # This view will be used to create a shopping cart for a client
    pass

def add_to_cart(request):
    # This view will be used to add items to the shopping cart
    pass

def view_cart(request):
    # This view will be used to view the contents of the shopping cart
    pass

def update_cart(request):
    # This view will be used to update the quantities of items in the shopping cart
    pass

def remove_from_cart(request):
    # This view will be used to remove items from the shopping cart
    pass

def checkout(request):
    pass

def delete_cart(request):
    # This view will be used to delete the shopping cart
    pass
