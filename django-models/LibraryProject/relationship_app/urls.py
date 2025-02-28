from django.urls import path
from . import views
from .views import register_view, login_view, logout_view
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView

from .views import admin_view, librarian_view, member_view

from .views import add_book, edit_book, delete_book, book_list

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    ]

urlpatterns = [
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]

urlpatterns = [
    path('add_book/', add_book, name='add_book'),  # Route for adding a book
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),  # Route for editing a book
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),  # Route for deleting a book
    path('books/', book_list, name='book_list'),  # Route to list books
]