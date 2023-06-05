from django.urls import path

from catalog.views import contacts, ProductListView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('contacts/', contacts)
]