from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library//<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")),  # Include relationship_app URLs
]


from django.urls import path
from .views import register, user_login, user_logout

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    
]

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views # import custom views


urlpatterns = [
    path("register/", views.register, name="register"),  # Registration page
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),  # Login page
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),  # Logout page
    path("", views.home, name="home"),  # Home page
]


#configuring url patterns for assgn3
from django.urls import path
from.views import admin_view, librarian_view, member_view

urlpatterns = [
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]

# defining url patterns for assgn 4
from django.urls import path
from .views import add_book, edit_book, delete_book

urlpatterns = [
    path("books/add_book/", add_book, name="add_book"),
    path("books/edit_book/<int:book_id>/", edit_book, name="edit_book"),
    path("books/delete_book/<int:book_id>/", delete_book, name="delete_book"),
]