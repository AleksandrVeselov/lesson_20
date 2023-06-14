from django.contrib import admin

from catalog.models import Category, Product, Blog


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для работы с моделью Category"""

    list_display = ['pk', 'title']  # Поля для отображения в админ-панели


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для работы с моделью Product"""

    list_display = ['pk', 'title', 'price', 'category']  # Поля для отображения в админ-панели
    list_filter = ('category',)  # Поля, по которым можно фильтровать записи
    search_fields = ('title', 'description')  # Поля, по которым производится поиск


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Админ-панель для работы с моделью Blog"""

    list_display = ['title', 'slug', 'content']  # Поля для отображения в админ-панели
    prepopulated_fields = {'slug': ('title',)}  # Поле для автоматического заполнения исходя из поля title

