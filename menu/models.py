from django.utils import timezone

from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField("Name", max_length=254, blank=False)
    price = models.IntegerField("Price", blank=False)
    date_added = models.DateField(default=timezone.now())
    image_url = models.CharField("Image URL", max_length=254, blank=False)
    description = models.CharField("Description", max_length=254, blank=False)

class MenuCategory(models.Model):
    name = models.CharField("Name", max_length=254, blank=False)