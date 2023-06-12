from django.contrib import admin

from catalog.models import Category, Product, Blog


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'price', 'category']
    list_filter = ('category',)
    search_fields = ('title', 'description')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'content']
    prepopulated_fields = {'slug': ('title',)}
