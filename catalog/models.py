from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey('catalog.Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Blog(models.Model):
    """Модель записи в блоге"""
    title = models.CharField(max_length=50, verbose_name='Название')  # Заголовок
    slug = models.CharField(max_length=50, verbose_name='Slug')  # Slug (человекопонятный URL)
    content = models.TextField(verbose_name='Содержимое')  # Текст записи
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')  # Превью
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания (генерируется автоматически)
    is_published = models.BooleanField(default=False)  # Метка публикации статьи
    views_count = models.IntegerField(default=0)  # количество просмотров (по умолчанию 0)

    def __str__(self):
        return f'{self.title} {self.created_at}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
