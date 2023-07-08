from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from catalog.models import Category


def send_email_100(post_title):
    """Функция для отправки письма на электронную почту"""
    send_mail('Поздравляем!',  # Тема письма
              f"Дорогой администратор! Количество просмотров поста {post_title} достигло 100, мои поздравления",
              settings.EMAIL_HOST_USER,  # От кого письмо
              recipient_list=['aleksandr1990veselov@yandex.ru'])


def get_cashed_categories_list():
    """Функция для создания и кеширования списка категорий"""

    # Если кеширование включено
    if settings.CACHE_ENABLED:
        key = 'categories'  # ключ, по которому можно получить данные из кеша
        categories_list = cache.get(key)  # пробуем получить данные из кеша

        # если там по ключу key ничего нет
        if categories_list is None:
            categories_list = Category.objects.all()  # выборка категорий
            cache.set(key, categories_list)  # запись в кеш

    # если кеширование выключено
    else:
        categories_list = Category.objects.all()  # выборка категорий
    return categories_list
