from django.db import models
from slugify import slugify


class Product(models.Model):
    """Модель продукты"""

    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey('catalog.Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания (генерируется автоматически)
    modified_at = models.DateTimeField(auto_now=True)  # Дата изменения (генерируется автоматически)

    def __str__(self):
        """Строковое представление"""
        return f'{self.title} {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


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

    # def __init__(self, *args, **kwargs):
    #     """Переопределение метода __init__ для автоматического формирования слага"""
    #     super().__init__(*args, **kwargs)
    #     self.slug = slugify(self.title)
    #     save = self.save()

    def save(self, *args, **kwargs):
        """Переопределение метода для автоматического формирования слага"""
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
