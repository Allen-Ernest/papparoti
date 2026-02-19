from django.urls import path
from . import views

urlpatterns = [
    path('view_menus/', views.get_menus, name='menus'),
    path('add_menu/', views.add_menu, name='add_menu'),
]