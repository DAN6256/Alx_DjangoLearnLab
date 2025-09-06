from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views import View

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
    


# def user_login(request):
#     """
#     Handles user login using Django's AuthenticationForm.
#     """
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('book-list')  # Redirect to a meaningful page
#     else:
#         form = AuthenticationForm()
#     return render(request, 'relationship_app/login.html', {'form': form})

# def user_logout(request):
#     """
#     Logs out the current user and renders a confirmation page.
#     """
#     logout(request)
#     return render(request, 'relationship_app/logout.html')

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


