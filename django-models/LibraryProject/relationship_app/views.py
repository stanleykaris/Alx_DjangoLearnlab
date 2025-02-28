from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Book

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

from django.views.generic.detail import DetailView
from .models import Library

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "relationship_app/home.html")


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html" # this will be the template we shall use to render the output
    context_object_name = "library"


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home") #redirect user to homepage
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})
    
def user_logout(request):
    logout(request)
    return redirect("login")


# creating role based views for assn3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# we create functions to check user role
def is_admin(user):
    return user.is_autheticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_autheticated and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_autheticated and user.userprofile.role == 'Member'

# we create views restricted to roles
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

# Adding restricting access based on permissions asgn 4
from django.shortcuts import render, get_list_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm # we assume we have a bookform to handle book input

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
            return redirect ("book_list")
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