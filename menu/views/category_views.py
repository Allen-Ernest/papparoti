from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from ..models import MenuCategory


@user_passes_test(
    lambda user: user.is_authenticated and user.role == 'admin',
    login_url='auth_admin',
)
@require_POST
def add_menu_cartegory(request):
    name = request.POST.get("name", "").strip()
    if not name:
        messages.error(request, "Enter a category name.")
        return redirect("menu_manager")

    MenuCategory.objects.create(name=name)
    messages.success(request, "Category created successfully.")
    return redirect("menu_manager")