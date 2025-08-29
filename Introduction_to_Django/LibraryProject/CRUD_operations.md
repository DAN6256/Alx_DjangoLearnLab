Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
#<Book: Book object (1)>


p =Book.objects.get(
pk=1)
>>> p.title
'1984'
>>> p.author
'George Orwell'
>>> p.publication_year
1949


p.title = "Nineteen 
Eighty-Four"
>>> p.title
'Nineteen Eighty-Four'

>>> p.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
<QuerySet []>