from django.urls import path

from catalog.views import ProductListView, ContactsListView, BlogList, BlogDetailView, BlogCreatePost, BlogUpdatePost, \
    BlogDeletePost

urlpatterns = [
    path('', ProductListView.as_view()),
    path('contacts/', ContactsListView.as_view()),
    path('blog/', BlogList.as_view()),
    path('blog/<slug:slug>/', BlogDetailView.as_view()),
    path('create_post/', BlogCreatePost.as_view()),
    path('update_post/<slug:slug>/', BlogUpdatePost.as_view()),
    path('delete_post/<slug:slug>/', BlogDeletePost.as_view())
]
