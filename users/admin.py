from django.contrib import admin

from users.models import User

admin.site.register(User)  # регистрация модели пользователя в админ-панели
