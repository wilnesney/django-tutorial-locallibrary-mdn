# Note: This file is custom (i.e., was not auto-generated).

from django.urls import path
from . import views

'''In path('', views.index, name='index'),
    views.index is a function.
    name='index' gives this URL mapping a unique name that lets us "reverse" the mapper, 
                i.e., dynamically create a URL that points to the resource 
                the mapper is designed to handle:
                <a href="{% url 'index' %}">Home</a>.
'''
'''The view for BookListView is implemented as a class. Calling as_view() on it 
    creates an instance of the class and ensures the right handler methods are called 
    for incoming HTTP requests. 
    This view will inherit from an existing generic view function that does most of what we want.'''

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    # int-format string param named 'pk' (expected by class)
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),  
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksListView.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]