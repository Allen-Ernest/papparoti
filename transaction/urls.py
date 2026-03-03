from . import views
from django.urls import path

urlpatterns = [
    path('order_success/<int:order_id>/', views.get_success_page, name='order_success'),
    path('order_error/', views.get_error_page, name='order_success'),
]