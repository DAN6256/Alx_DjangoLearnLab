from .models import Book, Library, Librarian, Author

# All books
#books = Book.objects.all()

# Books by author name
books_by_author_name = Book.objects.filter(name="Some author")


# Books in a specific library (get a Library instance first)
library = Library.objects.get(pk=1)  
books_in_library = library.books.all()

# Retrieve the librarian for that library
librarian = library.librarian  
# Or: librarian = Librarian.objects.get(library=library)