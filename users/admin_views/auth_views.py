from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import User, AdminProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required()
def get_admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def get_admin_register(request):
    return render(request, 'admin_auth.html')


def register_admin(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error("Passwords don't match")
            return redirect('auth_admin')

        if first_name and last_name and email and password:
            user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name,
                                            role='admin')
            AdminProfile.objects.create(user=user)
            return redirect('auth_admin')
        else:
            messages.error(request, 'Please insert correct info')
            return redirect('auth_admin')
    else:
        return render(request, 'auth_admin')


def login_admin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None and user.role == 'admin':
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('auth_admin')

    else:
        messages.error(request, 'Invalid Request')
        return redirect('auth_admin')
