from ..models import Menu, MenuCategory
from django.shortcuts import redirect

def add_menu_cartegory(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            menu_category = MenuCategory.objects.create(name=name)
            menu_category.save()
            return redirect("menu_manager")
        else:
            context = {"Error": "Invalid Request"}
            return redirect("menu_manager")
    else:
        context = {"Error": "Bad Request"}
        return redirect("menu_manager")