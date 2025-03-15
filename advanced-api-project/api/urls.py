from django.urls import path
from .views import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,

)

urlpatterns = [
    path('books/list/', ListView.as_view(), name='book-list'),
    path('books/detail/<int:pk>/', DetailView.as_view(), name='book_detail'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/update/', UpdateView.as_view(), name='book-update'),
    path('books/delete/', DeleteView.as_view(), name='book-delete'),
]