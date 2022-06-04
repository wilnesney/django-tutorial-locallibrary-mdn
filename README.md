# Local Library Django tutorial (from MDN)

This code is based on the Mozilla Developer Network (MDN) Django tutorial, found here:
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django

Left off here:
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms#modelforms

This readme includes some commonly-used commands and process stuff. It is not an overview of how to use Django.

Note: Use "py" for Windows, "python3" for Linux

## Virtual environment
	pip3 install virtualenvwrapper-win		# One-time install, to make virtual enviroments
	mkvirtualenv my_django_environment		# Create a virtual env called my_django_environment
* When working in a virtual env., env. indicated by:
* (my_django_environment) D:\dave\>

### Common virtual environment-related commands:
    deactivate — Exit out of the current Python virtual environment
    workon — List available virtual environments
    workon name_of_environment — Activate the specified Python virtual environment
    rmvirtualenv name_of_environment — Remove the specified environment.

## Installing Django
	pip3 install django~=4.0
	py -m django --version		# Verify installation

## Starting New Django Project
	mkdir django_test
	cd django_test
	django-admin startproject mytestsite	# Create skeleton site
	cd mytestsite
	py manage.py runserver  
Development server, at default 127.0.0.1:8000. Can specify custom IP/port.
* E.g., django-admin runserver 1.2.3.4:8000
* See https://docs.djangoproject.com/en/4.0/ref/django-admin/#runserver
* Then use browser to go to http://127.0.0.1:8000/
	
## Adding Django Application
Assuming the name of the application we want to add is "catalog"

	py manage.py startapp catalog	# Create "catalog" application. Run in same folder as manage.py.
Add 'catalog.apps.CatalogConfig' (from /catalog/apps.py) to settings.py's INSTALLED_APPS to register it
 
## Specify the Database
* See https://docs.djangoproject.com/en/4.0/ref/settings/#databases
* Configured in settings.py > DATABASES. Uses SQLite as default (no extra setup required with that).

## Use a Custom User Model (not done in tutorial)
See https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

## Other Settings
### Time zone:
* settings.py > TIME_ZONE (e.g., TIME_ZONE = 'America/Los_Angeles')
* *Must* match computer's time zone on Windows machines
* See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
* See https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-TIME_ZONE
### For production:
* SECRET_KEY
* DEBUG: Set to False! Otherwise, errors will display debug logs instead of http status codes
		
## Hooking up to URL Mapper
Best to defer mappings to associated application
### Add a urls.py file to application folder. E.g., 
	from django.urls import path
	from . import views
	urlpatterns = [	]
### Add mapping in base project's urls.py, e.g., 
	from django.urls import include
	urlpatterns += [ path('catalog/', include('catalog.urls')) ]
	
## Running Database Migrations
* Must run these commands every time models change in way that'll affect structure of stored data!
* Django tracks changes to model definitions. 

	py manage.py makemigrations  # Creates migrations for all applications. 
Specify app name to create migrations for just that app.
	py manage.py migrate  # Applies the previously-created migrations

## Create a Superuser
	py manage.py createsuperuser  
* Will prompt for username, email address, and *strong* password.
* For test: dave, dave.turka@gmail.com, wrgmz^10
* (test_user for non-admin test account name)
							  
## Create a template Folder
* Create a folder called "templates" in the application folder. E.g., catalog/templates/
* This is the default location Django will check for templates for the application.
