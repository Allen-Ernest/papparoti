from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)

        extra_fields.setdefault("username", email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (("client", "Client"), ("admin", "Admin"))

    first_name = models.CharField("First Name", max_length=30, blank=False)
    middle_name = models.CharField("Middle Name", max_length=30, blank=True)
    last_name = models.CharField("Last Name", max_length=30, blank=False)
    email = models.EmailField("Email Address", max_length=254, blank=False, unique=True)
    role = models.CharField("Role", choices=ROLE_CHOICES, max_length=30, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    objects = CustomUserManager()

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    phone = models.CharField("Phone", max_length=30, blank=False, unique=True)

    def clean(self):
        if self.user.role != "client":
            raise ValueError("Only clients with role 'client' are allowed")

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    def clean(self):
        if self.user.role != 'admin':
            raise ValueError("Only admins with role 'admin' are allowed")