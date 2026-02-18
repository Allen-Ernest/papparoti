from django.urls import path
from . import views

urlpatterns = [
    path('add_menu/', views.add_menu, name='add_menu'),
]