from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    username = None  # имя пользователя (None - авторизация по email)
    email = models.EmailField(unique=True, verbose_name='Email')  # email

    phone = models.CharField(max_length=25, verbose_name='Телефон')  # номер телефона
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', blank=True, null=True)  # аватар
    country = models.CharField(max_length=100, verbose_name='Страна')  # страна

    USERNAME_FIELD = 'email'  # основное поле для авторизации
    REQUIRED_FIELDS = []

