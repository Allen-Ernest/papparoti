from . import views
from django.urls import path

urlpatterns = [
    path('checkout/', views.get_checkout_page, name='checkout'),
]