from pyexpat.errors import messages
from django.shortcuts import render, redirect
from ..models import Menu, MenuCategory
from django.utils import timezone

# Create your views here.
def get_menus(request):
    menus = Menu.objects.all()
    return render(request, "menu.html", {"menus": menus})

def get_menu_manager(request):
    menus = Menu.objects.all()
    categories = MenuCategory.objects.all()
    return render(request, "menu_management.html", {"menus": menus, "categories": categories})

def add_menu(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        img = request.POST.get("image")
        category_id = request.POST.get("category")

        if name and price and description and img and category_id:
            try:
                category = MenuCategory.objects.get(id=category_id)
                menu = Menu.objects.create(name=name, price=price, description=description, image_url=img, category=category)
                menu.save()
                return redirect("menu_manager")
            except MenuCategory.DoesNotExist:
                messages.error(request, 'Invalid Request')
                return redirect("menu_manager")
        else:
            messages.error(request, 'Invalid Request')
            return redirect("menu_manager")
    else:
        messages.error(request, 'Invalid Request')
        return redirect("admin_dashboard")

def delete_menu(request):
    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        if menu_id:
            menu = Menu.objects.get(id=menu_id)
            menu.delete()
            return render(request, "menu.html", {"menus": [menu]})
        else:
            return render(request, "menu.html", {"menus": []})

    else:
        context = {"Error": "Bad Request"}
        return render(request, "menu.html")
    
def update_menu(request):
    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        img = request.POST.get("image")

        if menu_id and name and price and description and img:
            try:
                menu = Menu.objects.get(id=menu_id)
                menu.name = name
                menu.price = price
                menu.description = description
                menu.image_url = img
                menu.save()
                return redirect("admin_dashboard")
            except Menu.DoesNotExist:
                context = {"Error": "Menu not found"}
                return redirect("admin_dashboard")
        else:
            context = {"Error": "Invalid Request"}
            return redirect("admin_dashboard")
    else:
        context = {"Error": "Bad Request"}
        return redirect("admin_dashboard")