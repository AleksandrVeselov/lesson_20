from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product, Blog
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
    model = Blog
    extra_context = {'title': 'Блог'}

    def get_queryset(self):
        """Отбор постов у которых is_published=True"""
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        object = super().get_object()
        object.views_count += 1
        if object.views_count == 100:
            send_email_100(object.title)
        object.save()
        return object


class BlogCreatePost(CreateView):
    model = Blog
    fields = ('title', 'slug', 'content', 'image', 'is_published')
    success_url = '/blog/'


class BlogUpdatePost(UpdateView):
    model = Blog
    fields = ('title', 'slug', 'content', 'image', 'is_published')

    def get_success_url(self, *args, **kwargs):
        slug = self.kwargs['slug']
        url = reverse_lazy('catalog:blog_post', args=[slug])

        return url


class BlogDeletePost(DeleteView):
    model = Blog
    success_url = '/blog/'
