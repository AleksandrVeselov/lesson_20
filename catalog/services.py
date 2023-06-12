from django.conf import settings
from django.core.mail import send_mail


def send_email_100(post_title):
    send_mail('Поздравляем!',
              f"Дорогой администратор! Количество просмотров поста {post_title} достигло 100, мои поздравления",
              settings.EMAIL_HOST_USER,
              recipient_list=['aleksandr1990veselov@yandex.ru'],
              fail_silently=False)
