from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.get_client_login_page, name='auth'),
    #path('auth/logout/', views.logout_user, name='logout'),
    path('auth_admin/', views.register_admin, name='auth_admin'),
    path('', views.get_home_page, name='home'),
    path('register/', views.register_client, name='register_client'),
]