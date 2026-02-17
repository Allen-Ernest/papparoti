from django.shortcuts import render
from .models import Menu

# Create your views here.
def get_menus(request):
    menus = Menu.objects.all()
    return render(request, "menu.html", {"menus": menus})

def add_menu(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        img = request.POST.get("image")

        if name and price and description and img:
            menu = Menu.objects.create(name=name, price=price, description=description, img=img)
            menu.save()
            return render(request, "menu.html", {"menus": [menu]})
        else:
            context = {"Error": "Invalid Request"}
            return render(request, "menu.html", {"menus": []})
    else:
        context = {"Error": "Bad Request"}
        return render(request, "menu.html")

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
