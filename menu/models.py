from django.db import models

# Create your models here.
class Menu(models.Model):
    category = models.ForeignKey('MenuCategory', on_delete=models.CASCADE, related_name='menus')
    name = models.CharField("Name", max_length=254, blank=False)
    price = models.IntegerField("Price", blank=False)
    image_url = models.CharField("Image URL", max_length=254, blank=False)
    description = models.CharField("Description", max_length=254, blank=False)

class MenuCategory(models.Model):
    name = models.CharField("Name", max_length=254, blank=False)