from django.urls import path
from django.shortcuts import render, redirect
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# register
from . import views

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path

# logout
from django.contrib.auth.views import LogoutView

from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .forms import BookForm


# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})
 
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
      
def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after registration
            return redirect('home')  # Redirect to home page or another page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


from django.urls import path
from .views import register, user_login, user_logout

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]

from django.urls import path, include

urlpatterns = [
    path('', include('relationship_app.urls')),  # Include relationship_app URLs
]

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

from django.apps import AppConfig

class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'

    def ready(self):
        import relationship_app.signals

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

# Helper functions to check roles
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to book list after adding
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to book list after editing
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

# View to delete a book (restricted by "can_delete_book" permission)
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Redirect to book list after deletion
    return render(request, 'relationship_app/delete_book.html', {'book': book})