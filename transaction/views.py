from django.shortcuts import redirect, render
from django.contrib import messages

def get_checkout_page(request):
    if request.user.is_authenticated and request.user.role == 'client':
        return render(request, "checkout.html")
    else:
        messages.error(request, 'Unauthorized access.')
        return redirect("auth")
    
def process_checkout(request):
    if request.method == 'POST':
        # Process the checkout form data here
        # For example, you can create an order, save it to the database, etc.
        
        messages.success(request, 'Checkout successful!')
        return redirect('home')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('checkout')
    
    #TODO: Let the server accept floating value prices
    #TODO: Add to cut functionality via javascript http requests
    #TODO: Modify order model
    #TODO: use the created error templates for any system errors