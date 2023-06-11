from django.urls import path

from catalog.views import ProductListView, ContactsListView, BlogList

urlpatterns = [
    path('', ProductListView.as_view()),
    path('contacts/', ContactsListView.as_view()),
    path('blog/', BlogList.as_view())
]
