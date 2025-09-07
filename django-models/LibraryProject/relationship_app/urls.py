from django.urls import path
from .views import CustomLoginView, CustomLogoutView, register, list_books, LibraryDetailView, views
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view
from .views import list_books
urlpatterns = [
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('login/', CustomLoginView.as_view(template_name="relationship_app/login.html"), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),
    path('register/', views.register, name='register'),
    path('admin-area/', admin_view.admin_view, name='admin-view'),
    path('librarian-area/', librarian_view.librarian_view, name='librarian-view'),
    path('member-area/', member_view.member_view, name='member-view'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete-book'),
]
