from django.urls import path
from .views import CustomLoginView, CustomLogoutView, register, list_books, LibraryDetailView, views

urlpatterns = [
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('login/', CustomLoginView.as_view(template_name="relationship_app/login.html"), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),
    path('register/', views.register, name='register'),
]
