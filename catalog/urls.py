from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactsListView, BlogList, BlogDetailView, BlogCreatePost, BlogUpdatePost, \
    BlogDeletePost, ProductCreateView, ProductUpdateView, ProductDeleteView, VersionListView, \
    ProductUpdateViewModerator, categories_list

app_name = CatalogConfig.name

urlpatterns = [
    path('', cache_page(60)(ProductListView.as_view()), name='home'),  # http://127.0.0.1:8000/ Главная страница
    path('contacts/', ContactsListView.as_view(), name='contacts'),  # http://127.0.0.1:8000/contacts/  Контакты
    path('blog/', BlogList.as_view(), name='blog'),  # http://127.0.0.1:8000/blog/  Список статей блога
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_post'),  # http://127.0.0.1:8000/blog/<slug>
    path('create_post/', BlogCreatePost.as_view(), name='create_post'),  # http://127.0.0.1:8000/create_post/
    path('update_post/<slug:slug>/', BlogUpdatePost.as_view(), name='update_post'), # http://127.0.0.1:8000/update_post/
    path('delete_post/<slug:slug>/', BlogDeletePost.as_view(), name='delete_post'), # http://127.0.0.1:8000/delete_post/
    path('create/', ProductCreateView.as_view(), name='create_product'),  # http://127.0.0.1:8000/create/
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),  # http://127.0.0.1:8000/update/<pk>
    path('update/<int:pk>/moderator', ProductUpdateViewModerator.as_view(), name='update_moderator'),  # редактирование продукта для модератора
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),  # http://127.0.0.1:8000/delete/<pk>
    path('versions/<int:pk>', VersionListView.as_view(), name='version'),  # http://127.0.0.1:8000/versions/<pk>
    path('categories/', categories_list, name='categories')
]
