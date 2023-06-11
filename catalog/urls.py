from django.urls import path

from catalog.views import ProductListView, ContactsListView, BlogList, BlogDetailView, BlogCreatePost

urlpatterns = [
    path('', ProductListView.as_view()),
    path('contacts/', ContactsListView.as_view()),
    path('blog/', BlogList.as_view()),
    path('blog/<slug>/', BlogDetailView.as_view()),
    path('blog/create/', BlogCreatePost.as_view())
]
