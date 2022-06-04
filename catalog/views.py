from django.shortcuts import render

# Everything from here down is added/custom.

from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

from catalog.forms import RenewBookForm

def index(request):
    '''View function for the site home page.'''

    # Generate counts of some of the main objects.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available book instances.
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Other stuff ("Challenge yourself")
    num_goosebumps = Book.objects.filter(title__startswith='Goosebumps').count()
    num_mg_horror = Book.objects.filter(
            genre__name__exact='Horror'
        ).filter(
            genre__name__exact='Middle Grade'
        ).count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_goosebumps': num_goosebumps,
        'num_mg_horror': num_mg_horror,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)


# Will query database to get all records for the model (Book).
# Will render a template at /locallibrary/catalog/templates/catalog/book_list.html [sic].
# Within template, can access list of books with template variable object_list or book_list (<the model name>_list).
#   Note: object_list and book_list are aliases for the same thing--either works.
# Minimum to set is the model. Can further customize with attributes and overriden methods.
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    # context_object_name = 'book_list'
    # queryset = Book.objects.filter(title__startswith='Goosebumps')[:5]  # 5 Goosebumps books 
    # template_name = 'books/my_arbitrary_template_name_list.html' 

    '''
    # Overriding get_queryset() is more flexible than just setting queryset.
    def get_queryset(self):
        return Book.objects.filter(title__startswith='Goosebumps')[:5]

    # Override get_context_data() to add whatever you want to the context.
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Add any extra data you want to the context
        context['some_data'] = 'This is just some data'
        return context
    '''

# Expects a template at /locallibrary/catalog/templates/catalog/book_detail.html [sic].
# Expects the book id passed as a parameter called 'pk' (short for Primary Key).
# Will pass template variable named object and book (i.e., <model_name>)--both will work.
class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author

# Note: LoginRequiredMixin must be listed first in inheritance list.
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    '''Generic class-based view listing books on loan to current user.'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
                borrower=self.request.user
            ).filter(
                status__exact='o'
            ).order_by(
                'due_back'
            )


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    '''Generic class-based view for librarians to see and return checked-out books.'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(
            status__exact='o'
        ).order_by(
            'due_back'
        )


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = RenewBookForm(request.POST)  # Create form instanced populated with request data (binding)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed'))

    # If this is a GET (or anything other than POST), create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
        