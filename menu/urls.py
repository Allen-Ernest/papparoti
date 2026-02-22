from django.urls import path
from .views import views
from .views import category_views

urlpatterns = [
    path('view_menus/', views.get_menus, name='menus'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('delete_menu/', views.delete_menu, name='delete_menu'),
    path('update_menu/', views.update_menu, name='update_menu'),
    path('menu_manager/', views.get_menu_manager, name='menu_manager'),
    path('add_menu_category/', category_views.add_menu_cartegory, name='add_menu_category'),
]