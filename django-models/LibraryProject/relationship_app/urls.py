from django.urls import path, include
from .views import list_books, LibraryDetailView, register, user_logout, user_login, admin_view, librarian_view, member_view, add_book, edit_book, delete_book
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from . import views

urlpatterns = [
    path('books/', list_books, name="list_books"),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name="library_detail"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")), # Include the urls from the relationship_app
]

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("", views.home, name="home"),
]

urlpatterns = [
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]

urlpatterns = [
    path("books/add_book/", add_book, name="add_book"),
    path("books/edit_book/<int:book_id>/", edit_book, name="edit_book"),
    path("books/delete_book/<int:book_id>/", delete_book, name="delete_book"),
]