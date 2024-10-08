from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomerManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password, needs_adverticing):
        if not username:
            raise ValueError("Username must be provided!")
        if not email:
            raise ValueError("Email must be provided!")
        customer = self.model(username=username, email=email, first_name=first_name, last_name=last_name, needs_adverticing=needs_adverticing)
        customer.set_password(password)
        customer.save()
        return customer

    def create_superuser(self, username, first_name, last_name, password):
        customer = self.create_user(username, "example@gmail.com", first_name, last_name, password, False)
        customer.is_admin = True 
        customer.is_staff = True
        customer.is_superuser = True
        customer.save()
        return customer


class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, validators=[MinLengthValidator(3)], unique=True, verbose_name="Никнейм")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Почта")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    needs_adverticing = models.BooleanField(default=False, verbose_name="Участие в рассылках")

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'needs_adverticing']


    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"