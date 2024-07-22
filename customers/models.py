from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomerManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password):
        if not username:
            raise ValueError("Username must be provided!")
        customer = self.model(username=username, first_name=first_name, last_name=last_name)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer

    def create_superuser(self, username, first_name, last_name, password):
        customer = self.create_user(username, first_name, last_name, password)
        customer.is_admin = True 
        customer.is_staff = True
        customer.is_superuser = True
        customer.save(using=self._db)
        return customer


class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, validators=[MinLengthValidator(3)], unique=True, verbose_name="Никнейм")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"