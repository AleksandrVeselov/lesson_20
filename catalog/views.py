from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductFormModerator
from catalog.models import Product, Blog, Version
from catalog.services import send_email_100


# def home(request):
#     products_list = Product.objects.all()
#     context = {'object_list': products_list}
#     return render(request, 'catalog/home.html', context)

class ProductListView(ListView):
    """Класс-контроллер для страницы со списком продуктов"""
    model = Product  # Модель с которой он работает
    extra_context = {'title': 'Список товаров'}  # Заголовок страницы


# def contacts(request):
#     if request.method == 'POST':
#         print(request.POST)
#     return render(request, 'catalog/contacts.html')


class ContactsListView(TemplateView):
    """Класс-контроллер страницы с контактами"""
    template_name = 'catalog/contacts.html'  # Шаблон для отображения


class BlogList(ListView):
    """Класс-контроллер для страницы со списком постов блога"""
    model = Blog  # Модель с которой он работает
    extra_context = {'title': 'Блог'}  # Заголовок страницы

    def get_queryset(self):
        """Отбор постов у которых is_published=True для отображения на странице"""

        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Класс-контроллер для детального отображения информации о посте"""

    model = Blog  # модель, с которой он работает

    def get_object(self, queryset=None):
        """Переопределение метода get_object для увеличения количества просмотров"""

        object = super().get_object()
        object.views_count += 1  # увеличение количества просмотров

        # Проверка, есть ли 100 просмотров у поста
        if object.views_count == 100:
            send_email_100(object.title)  # Отправка сообщения на почту 'aleksandr1990veselov@yandex.ru'

        object.save()  # сохранение в базе данных

        return object


class BlogCreatePost(CreateView):
    """Класс-контроллер для отображения страницы с формой создание поста"""

    model = Blog  # Модель с которой он работает
    fields = ('title', 'content', 'image', 'is_published')  # Поля для построения формы
    success_url = '/blog/'  # URL адрес, на который происходит перенаправление после успешного создания записи в блоге


class BlogUpdatePost(UpdateView):
    """Класс-контроллер для отображения формы изменение записи"""
    model = Blog  # Модель, с которой он работает
    fields = ('title', 'content', 'image', 'is_published')  # поля для отображения в форме

    def get_success_url(self, *args, **kwargs):
        """Переопределение метода get_success_url для формирования правильного URL на который происходит
        перенаправление после успешного изменения записи блога"""

        slug = self.kwargs['slug']  # slug статьи
        url = reverse_lazy('catalog:blog_post', args=[slug])  # формирование URL

        return url


class BlogDeletePost(DeleteView):
    """Класс-контроллер для удаления записи в блоге"""
    model = Blog  # Модель, с которой он работает
    success_url = '/blog/'  # URL адрес, на который происходит перенаправление после успешного удаления записи в блоге


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс-контроллер для создания продукта
    LoginRequiredMixin - только для авторизованных пользователей"""

    model = Product  # Модель, с которой он работает
    form_class = ProductForm  # Форма для заполнения

    # URL адрес, на который происходит перенаправление после успешного удаления записи в блоге
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Добавление в создаваемый продукт информации об авторизованном пользователе"""

        product = form.save()  # Сохранение информации о созданном продукте
        product.owner = self.request.user  # присваивание атрибуту owner
        product.save()  # сохранение
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс-контроллер для редактирования продукта
    LoginRequiredMixin - только для авторизованных пользователей
    PermissionRequiredMixin - только для пользователей с указанными правами"""

    model = Product  # Модель, с которой он работает
    form_class = ProductForm  # Форма для заполнения

    permission_required = 'catalog.сan_change_description'

    def get_context_data(self, **kwargs):
        """Переопределение метода get_context_data, добавление в контекст формсета"""

        context_data = super().get_context_data(**kwargs)

        # 1-Родительская модель 2-модель дочерняя 3-модель формы extra-количество новых форм
        ParentFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)

        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        """В случае успешного заполнения формы перенаправление на страницу с версиями соответствующего продукта"""

        return reverse('catalog:version', args=[self.kwargs.get('pk')])


class ProductUpdateViewModerator(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс-контроллер для редактирования продукта модератором
        LoginRequiredMixin - только для авторизованных пользователей
        PermissionRequiredMixin - только для пользователей с указанными правами"""

    model = Product  # Модель, с которой он работает
    form_class = ProductFormModerator  # Форма для заполнения

    permission_required = 'catalog.сan_change_description'

    def get_success_url(self, **kwargs):
        """В случае успешного заполнения формы перенаправление на страницу с версиями соответствующего продукта"""

        return reverse('catalog:version', args=[self.kwargs.get('pk')])


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс-контроллер для удаления продукта, с применением миксинов
    LoginRequiredMixin - только для авторизованных пользователей
    PermissionRequiredMixin - только для пользователей с указанными правами"""

    model = Product  # Модель, с которой он работает
    # URL адрес, на который происходит перенаправление после успешного удаления записи в блоге
    success_url = reverse_lazy('catalog:home')

    permission_required = 'catalog.Can delete Продукт'  # права пользователей


class VersionListView(ListView):
    """Класс-контроллер для отображения списка активных версии текущего продукта"""
    model = Version

    def get_queryset(self, *args, **kwargs):
        """Переопределение метода get_queryset для возможности отфильтровать активные версии продукта с нужным id"""

        product_pk = self.kwargs.get('pk')  # получение id продукта
        return Version.objects.filter(is_active=True, product_id=product_pk)

    def get_context_data(self, *args, object_list=None, **kwargs):
        """Переопределение метода get_context_data для передачи в шаблон и отображения на странице
         наименования продукта"""

        product = Product.objects.get(pk=self.kwargs.get('pk'))  # Получение продукта с соответствующим id
        context = super().get_context_data(*args, **kwargs)  # получение контекста
        context['product_title'] = product.title  # добавление в контекст наименования продукта
        context['pk'] = product.pk  # добавление в контекст id продукта
        return context
