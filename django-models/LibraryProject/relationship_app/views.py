from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Book,Library
# Create your views here.


def list_books(request):
    """
    Function-based view to list all books and their authors.
    Returns a plain text response with each book on a new line.
    """
    books = Book.objects.select_related('author').all()
    output_lines = [f"{book.title} by {book.author.name}" for book in books]
    response_text = "\n".join(output_lines)
    return HttpResponse(response_text, content_type="text/plain")


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
