from django.db import models
from django.forms import forms
from slugify import slugify

from config import settings


class Product(models.Model):
    """Модель продукты"""

    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey('catalog.Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания (генерируется автоматически)
    modified_at = models.DateTimeField(auto_now=True)  # Дата изменения (генерируется автоматически)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)  # Владелец
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')

    def __str__(self):
        """Строковое представление"""
        return f'{self.title}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = (('сan_change_description', 'can change description'),
                       ('сan_change_category', 'can change category'),
                       ('сan_change_is_published', 'can change is_published'),
                       ('сan_view_price', 'can view price'))


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')  # название категории
    description = models.TextField(blank=True, null=True, verbose_name='Описание')  # описание категории

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Blog(models.Model):
    """Модель записи в блоге"""
    title = models.CharField(max_length=50, verbose_name='Название')  # Заголовок
    slug = models.SlugField(max_length=50, verbose_name='Slug')  # Slug (человекопонятный URL)
    content = models.TextField(verbose_name='Содержимое')  # Текст записи
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')  # Превью
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания (генерируется автоматически)
    is_published = models.BooleanField(default=False)  # Метка публикации статьи
    views_count = models.IntegerField(default=0)  # количество просмотров (по умолчанию 0)

    def __str__(self):
        """Строковое представление"""
        return f'{self.title} {self.created_at}'

    def save(self, *args, **kwargs):
        """Переопределение метода для автоматического формирования слага"""
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Version(models.Model):
    """Модель Версия продукта"""
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, verbose_name='Продукт')  # Продукт
    number = models.IntegerField(verbose_name='Номер версии', unique=True)
    title = models.CharField(max_length=100, verbose_name='Название версии')
    description = models.TextField(verbose_name='Описание текущей версии', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активность')

    def __str__(self):
        return f'Продукт {self.product} версии {self.title}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

