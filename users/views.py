from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, ClientProfile

def get_home_page(request):
    return render(request, 'home.html')

def get_client_login_page(request):
    return render(request, 'auth.html')

def login_client(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None and user.role == 'client':
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        messages.error(request, "Bad request")
        return redirect('auth')

def register_client(request):
    if request.method == "POST":
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('auth')

        if email is not None and password is not None and first_name is not None and last_name is not None and phone is not None:
            user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role='client')
            ClientProfile.objects.create(user=user, phone=phone)
            return redirect('auth')
        else:
            messages.error(request, 'Please enter correct Info')
            return redirect('auth')

    else:
        messages.error(request, 'Internal Server error')
        return redirect('auth')

def login_client(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None and user.role == 'client':
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('auth')

def logout_user(request):
    logout(request)
    return redirect('auth')

def get_client_profile(request):
    if request.user.is_authenticated and request.user.role == 'client':
        profile = ClientProfile.objects.get(user=request.user)
        return render(request, 'profile.html', {'profile': profile})
    else:
        messages.error(request, 'Unauthorized Access')
        return redirect('auth')