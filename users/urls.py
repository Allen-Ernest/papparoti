from django.urls import path
from . import views
from .admin_views import auth_views

urlpatterns = [
    path('auth/', views.get_client_login_page, name='auth'),
    path('auth/login', views.login_client, name='login_client'),
    path('client_profile/', views.get_client_profile, name='client_profile'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth_admin/', auth_views.get_admin_register, name='auth_admin'),
    path('register_admin/', auth_views.register_admin, name='register_admin'),
    path('login_admin/', auth_views.login_admin, name='login_admin'),
    path('admin_dash/', auth_views.get_admin_dashboard, name='admin_dashboard'),
    path('', views.get_home_page, name='home'),
    path('register/', views.register_client, name='register_client'),
]