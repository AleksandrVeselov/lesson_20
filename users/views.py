import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    """Класс-представление для создания пользователя"""
    model = User  # модель с которой он работает
    form_class = UserRegisterForm  # форма для отображения
    template_name = 'users/register.html'  # шаблон
    success_url = reverse_lazy('users:login')  # адрес для перенаправления


class ProfileView(UpdateView):
    """класс-представление для редактирования пользователя"""
    model = User  # модель с которой он работает
    form_class = UserProfileForm  # форма для отображения
    success_url = reverse_lazy('users:profile')  # адрес для перенаправления

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    """Функция для генерации случайного пароля"""
    new_password = ''.join([str(random.randint(0, 9)) for i in range(12)])  # новый случайный пароль
    request.user.set_password(new_password)  # установление пользователю нового пароля
    # print(new_password)
    send_mail(subject='Вы сменили пароль',
              message=f'Ваш новый пароль - {new_password}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[request.user.email])  # отправка письма на почту с новым паролем
    request.user.save()  # сохранение
    return redirect(reverse('catalog:home'))


def activate_new_user(request, pk):
    """Функция для активации нового пользователя"""
    user = get_user_model()  # получение модели пользователя
    user_for_activate = user.objects.get(id=pk)  # получение пользователя с нужным id
    user_for_activate.is_active = True  # смена флага у пользователя на True
    user_for_activate.save()  # сохранение
    return render(request, 'users/activate_user.html')
