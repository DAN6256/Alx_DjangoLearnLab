from .models import Book, Library, Librarian, Author



# Books by author name
author_name = "Some author"
author = Author.objects.get(name=author_name)
books_by_author_name = Book.objects.filter(author=author)


# Books in a specific library (get a Library instance first)
library_name = "Some Library"  
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()

# Retrieve the librarian for that library
library_name# Or: librarian = Librarian.objects.get(library=library)