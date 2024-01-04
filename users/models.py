from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from catalog.models import NULLABLE

random_code = str(random.randint(00000000, 99999999))


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    confirm_code = models.CharField(max_length=8, default=random_code, verbose_name='Код подтверждения', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
