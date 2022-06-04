from django.contrib import admin

# Everything from here down is custom/added.
# This file is used to register models for the admin site.

from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

# The above is all you need for a basic admin site (with everything's registration uncommented).
# Everything that follows adds quality of life improvements, etc.

# See below with BookInstanceInlines for details on Inlines.
class BookInlines(admin.StackedInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    # list_display attribute tuple specifies what to show and in what order
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # fields attribute lists what will display on the form, in order.
    # Vertical display by default, with further grouping displayed horizontally (birth/death tuple)
    # Could instead use the 'exclude' attribute to declare list of attributes to *not* show 
    # (everything else will be shown)
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInlines]

admin.site.register(Author, AuthorAdmin)


# Inlines allow you to add associated records at same time (e.g., BookInstance on Book page).
# TabularInline is for horizontal layout, StackedInline for vertical.
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # Don't have spare BookInstances (default is 3 ready to fill out).

# Using the @admin.register decorator is equivalent to calling admin.site.register(Book, BookAdmin)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    '''Can't directly specify the genre field in list_display because 
    it is a ManyToManyField (Django prevents this because 
    there would be a large database access "cost" in doing so). 
    Instead we'll define a display_genre function to get the information as a string.

    Note: Getting the genre may not be a good idea here, because of the "cost" of the database operation.
    We're showing you how because calling functions in your models can be very useful 
    for other reasons — for example to add a Delete link next to every item in the list.'''
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

#admin.site.register(Book, BookAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    # Use fieldsets attribute to group related information in the detail form.
    # Each section has its own title (or None, if you don't want one) and associated tuple
    # of fields in a dictionary.
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        })
    )