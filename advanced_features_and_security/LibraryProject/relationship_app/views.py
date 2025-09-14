from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Library
from .models import Book

# Function-based view to list all books
def list_books(request):
    """
    Renders a list of all books and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to show details of a specific library
class LibraryDetailView(DetailView):
    """
    Displays details for a specific Library, including all associated Books.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.select_related('author').all()
        return context
    




def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

def register(request):
    """
    Handles user registration using Django's UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book-list')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Class-based login view using Django's AuthenticationForm.
    Redirects to 'book-list' on successful login.
    """
    template_name = 'relationship_app/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return redirect('book-list').url


class CustomLogoutView(LogoutView):
    """
    Class-based logout view that renders a confirmation page.
    """
    template_name = 'relationship_app/logout.html'

from django.contrib.auth.decorators import permission_required
from .forms import BookForm  # Make sure you have a ModelForm for Book

@permission_required('relationship_app.can_add_book')
def add_book(request):
    """
    Allows authorized users to add a new book.
    """
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book-list')
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    """
    Allows authorized users to edit an existing book.
    """
    book = get_object_or_404(Book, id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book-list')
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    """
    Allows authorized users to delete a book.
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})



