from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse
from .models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import BookForm

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

@login_required
def home(request):
    return render(request, "relationship_app/home.html")

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
    
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        
    else:
        form = AuthenticationForm()
        return render(request, "relationship_app/login.html", {"form": form})
    
def user_logout(request):
    logout(
        request
    )
    return redirect("login")

def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'

# Creating views restricted to roles
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
        else:
            form = BookForm()
        return render(request, "relationship_app/add_book.html", {"form": form})
    
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_list_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
        else:
            form = BookForm(instance=book)
        return render(request, "relationship_app/edit_book.html", {"form": form, "book": book})
    
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_list_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "relationship_app/delete_book.html", {"book": book})
