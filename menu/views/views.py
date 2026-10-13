from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from ..models import Menu, MenuCategory
from shopping_cart.models import Cart, CartItem


admin_required = user_passes_test(
    lambda user: user.is_authenticated and user.role == 'admin',
    login_url='auth_admin',
)

def get_menus(request):
    categories = MenuCategory.objects.prefetch_related('menus')
    menus = Menu.objects.select_related('category')
    cart_items_count = 0
    
    if request.user.is_authenticated and request.user.role == 'client':
        client_profile = request.user.client_profile
        cart = Cart.objects.filter(user=client_profile, status="active").first()
        if cart:
            cart_items_count = CartItem.objects.filter(cart=cart).count()
            cart_items_ids = CartItem.objects.filter(cart=cart).values_list('menu_id', flat=True)
            return render(request, "menu.html", {
            "menus": menus,
            "categories": categories,
            "cart_items_count": cart_items_count,
            "cart_items_ids": cart_items_ids
            })
        else:
            return render(request, "menu.html", {
            "menus": menus,
            "categories": categories,
            "cart_items_count": cart_items_count
            })
    else:
        return render(request, "menu.html", {
        "menus": menus,
        "categories": categories,
        "cart_items_count": cart_items_count
        })
        

@admin_required
def get_menu_manager(request):
    menus = Menu.objects.select_related('category').all()
    categories = MenuCategory.objects.all()
    return render(request, "menu_management.html", {"menus": menus, "categories": categories})


@admin_required
@require_POST
def add_menu(request):
    name = request.POST.get("name", "").strip()
    price = request.POST.get("price", "").strip()
    description = request.POST.get("description", "").strip()
    image_url = request.POST.get("image", "").strip()
    category_id = request.POST.get("category")

    if not all((name, price, description, image_url, category_id)):
        messages.error(request, "Please complete all menu item fields.")
        return redirect("menu_manager")

    try:
        price = int(price)
    except ValueError:
        messages.error(request, "Price must be a whole number of Tanzanian shillings.")
        return redirect("menu_manager")

    if price <= 0:
        messages.error(request, "Price must be greater than zero.")
        return redirect("menu_manager")

    category = get_object_or_404(MenuCategory, id=category_id)
    Menu.objects.create(
        name=name,
        price=price,
        description=description,
        image_url=image_url,
        category=category,
    )
    messages.success(request, "Menu item created successfully.")
    return redirect("menu_manager")


@admin_required
@require_POST
def delete_menu(request):
    menu_id = request.POST.get("menu_id")
    if not menu_id:
        messages.error(request, "Choose a menu item to delete.")
        return redirect("menu_manager")

    menu = get_object_or_404(Menu, id=menu_id)
    menu.delete()
    messages.success(request, "Menu item deleted successfully.")
    return redirect("menu_manager")


@admin_required
@require_POST
def update_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    name = request.POST.get("name", "").strip()
    price = request.POST.get("price", "").strip()
    description = request.POST.get("description", "").strip()
    image_url = request.POST.get("image", "").strip()
    category_id = request.POST.get("category")

    if not all((name, price, description, image_url, category_id)):
        messages.error(request, "Please complete all menu item fields.")
        return redirect("menu_manager")

    try:
        price = int(price)
    except ValueError:
        messages.error(request, "Price must be a whole number of Tanzanian shillings.")
        return redirect("menu_manager")

    if price <= 0:
        messages.error(request, "Price must be greater than zero.")
        return redirect("menu_manager")

    category = get_object_or_404(MenuCategory, id=category_id)
    menu.name = name
    menu.price = price
    menu.description = description
    menu.image_url = image_url
    menu.category = category
    menu.save()
    messages.success(request, "Menu item updated successfully.")
    return redirect("menu_manager")


def get_500_error(request):
    return render(request, "500.html")