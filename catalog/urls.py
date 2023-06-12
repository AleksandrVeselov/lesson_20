from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactsListView, BlogList, BlogDetailView, BlogCreatePost, BlogUpdatePost, \
    BlogDeletePost

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsListView.as_view(), name='contacts'),
    path('blog/', BlogList.as_view(), name='blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_post'),
    path('create_post/', BlogCreatePost.as_view(), name='create_post'),
    path('update_post/<slug:slug>/', BlogUpdatePost.as_view(), name='update_post'),
    path('delete_post/<slug:slug>/', BlogDeletePost.as_view(), name='delete_post')
]
