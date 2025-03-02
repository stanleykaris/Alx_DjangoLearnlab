from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, RegisterView

from .views import admin_view, librarian_view, member_view

from .views import add_book, edit_book, delete_book, book_list

urlpatterns = [
    path('', views.book_list_view, name='home'),
    path('', views.LibraryDetailView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    path('books/add_book/', add_book, name='add_book'),
    path('books/edit_book/<int:book_id>/', edit_book, name='edit_book'),
    path('books/delete_book/<int:book_id>/', delete_book, name='delete_book'),
    path('books/', book_list, name='book_list'),
    path('books/', list_books, name='book_list'),
]