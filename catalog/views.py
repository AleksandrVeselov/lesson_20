from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product, Blog


# def home(request):
#     products_list = Product.objects.all()
#     context = {'object_list': products_list}
#     return render(request, 'catalog/home.html', context)

class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Список товаров'}

#
# def contacts(request):
#     if request.method == 'POST':
#         print(request.POST)
#     return render(request, 'catalog/contacts.html')


class ContactsListView(TemplateView):
    template_name = 'catalog/contacts.html'


class BlogList(ListView):
    model = Blog
    extra_context = {'title': 'Блог'}

    def get_queryset(self):
        """Отбор постов у которых is_published=True"""
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog


class BlogCreatePost(CreateView):
    model = Blog
    fields = ('title', 'slug', 'content', 'image', 'is_published')
    success_url = '/blog/'


class BlogUpdatePost(UpdateView):
    model = Blog
    fields = ('title', 'slug', 'content', 'image', 'is_published')
    success_url = '/blog/'


class BlogDeletePost(DeleteView):
    model = Blog
    success_url = '/blog/'

