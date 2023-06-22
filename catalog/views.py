from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
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
    """Класс-контроллер для уделения записи в блоге"""
    model = Blog  # Модель, с которой он работает
    success_url = '/blog/'  # URL адрес, на который происходит перенаправление после успешного удаления записи в блоге


class ProductCreateView(CreateView):
    """Класс-контроллер для создания продукта"""
    model = Product  # Модель, с которой он работает
    form_class = ProductForm  # Форма для заполнения

    # URL адрес, на который происходит перенаправление после успешного удаления записи в блоге
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    """Класс-контроллер для редактирования продукта"""
    model = Product  # Модель, с которой он работает
    form_class = ProductForm  # Форма для заполнения

    # URL адрес, на который происходит перенаправление после успешного удаления записи в блоге
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(DeleteView):
    """Класс-контроллер для удаления продукта"""
    model = Product  # Модель, с которой он работает
    # URL адрес, на который происходит перенаправление после успешного удаления записи в блоге
    success_url = reverse_lazy('catalog:home')


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
        return context
