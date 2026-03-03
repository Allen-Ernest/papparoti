from django.urls import path
from . import views
from .order_management_views import order_manager_view

urlpatterns = [
    path('orders/', views.get_orders_page, name='orders'),
    path('order_manager/', order_manager_view.get_order_manager, name='order_manager'),
    path('checkout/', views.get_checkout_page, name='checkout'),
    path('make_pay/', views.process_order, name='make_payment'),
    path("/complete/<int:order_id>/", order_manager_view.complete_order, name="complete_order"),
    path("orders/update/<int:order_id>/<str:new_status>/", order_manager_view.update_order_status, name="update_order_status"),
]