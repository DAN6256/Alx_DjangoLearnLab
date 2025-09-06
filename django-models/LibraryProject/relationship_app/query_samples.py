from .models import Book, Library, Librarian, Author

# All books
#books = Book.objects.all()

# Books by author name
books_by_author_name = Book.objects.filter(name="Some author")


# Books in a specific library (get a Library instance first)
library_name = Library.objects.get(pk=1)  
books_in_library = Library.objects.get(name=library_name)

# Retrieve the librarian for that library
library_name# Or: librarian = Librarian.objects.get(library=library)