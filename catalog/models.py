from django.db import models

# Everything from here is custom/added.
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns (lookup by URL name)
import uuid  # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    '''Model representing a book genre.'''
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g., Science Fiction)')

    def __str__(self):
        '''String for representing the Model object.'''
        return self.name


class Language(models.Model):
    '''Model representing the language of a work.'''
    language = models.CharField(max_length=100, unique=True,
                                help_text="Enter the work's natural language (e.g., English, French)")

    def __str__(self):
        '''String for representing the Model object.'''
        return self.language


class Book(models.Model):
    '''Model representing a book (but not a specific copy/instance of a book).'''
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author (in this tutorial), 
    # but authors can have multiple books.
    # Author as string rather than object because it hasn't been declared yet in the file.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Note: max_length is enforced at the Django level, not the database level.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    # Explicitly naming isbn field as 'ISBN' to avoid it showing up as 'Isbn'
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13-Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # ManyToManyField used because genre can contain many books, books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        '''String for representing the Model object.'''
        return self.title

    def get_absolute_url(self):
        '''Returns the URL to access a detail record for this book.'''
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        '''Create a string for the Genre. Required to display genre in Admin.'''
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'  # For Admin UI


class BookInstance(models.Model):
    '''Model representing a specific copy of a book (i.e., that can be borrowed from the library).'''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                            help_text='Unique ID for this particular book across whole library')
    # Use on_delete=models.RESTRICT so you have to delete all book instances before you can delete the 
    # corresponding book.
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)  # Must be null/blank for checked-in books.
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']  # In queries, order by soonest-due first
        permissions = (('can_mark_returned', 'Set book as returned.'),)

    def __str__(self):
        '''String for representing the model object.'''
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back


class Author(models.Model):
    '''Model representing an author.'''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        '''Returns the URL to access a particular author instance.'''
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        '''String for representing the Model object.'''
        return f'{self.last_name}, {self.first_name}'