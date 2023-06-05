from django.shortcuts import render
from django.views.generic import ListView, DetailView

from catalog.models import Product


# def home(request):
#     products_list = Product.objects.all()
#     context = {'object_list': products_list}
#     return render(request, 'catalog/home.html', context)

class ProductListView(ListView):
    model = Product
    extra_context = {'title': 'Список товаров'}


def contacts(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'catalog/contacts.html')
