from django.conf import settings
from django.core.mail import send_mail


def send_email_100(post_title):
    """Функция для отправки письма на электронную почту"""
    send_mail('Поздравляем!',  # Тема письма
              f"Дорогой администратор! Количество просмотров поста {post_title} достигло 100, мои поздравления",
              settings.EMAIL_HOST_USER,  # От кого письмо
              recipient_list=['aleksandr1990veselov@yandex.ru'])
