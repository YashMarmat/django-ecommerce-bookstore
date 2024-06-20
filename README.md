<p id ="top" align="center">
  <img src="https://github.com/YashMarmat/Pages-App-django/blob/master/templates/django bookstore logo.png" width="90%">
</p>


# Django-Ecommece-Bookstore
<p>An online bookshop developed in django-3 which allow users to purchase books online :) </p>

<img src="https://github.com/YashMarmat/Pages-App-django/blob/master/templates/dj-ecom-bstore-pic2.png?raw=true">

### Live App
* checkout the site here: <a href="https://dj-bookstore.onrender.com/" target="_blank" >Deployed App</a> (little note below)

(Note: The website can take upto 30 seconds (hosted on Render free tier services), as the project has no clients, its just for learning, please refer the source
code to run locally).

### Short Note

This guide will Step-by-Step help you to create your own ecommerce bookstore application in django. With HTML, CSS, JAVASCRIPT and Django Framework. 

Note: this guide is not for absolute beginners so im assuming that you have the basic knowledge of MVT in django to get started. To know more on it i recommend you <a href="https://docs.djangoproject.com/en/3.0/">django documentation</a>.

# Table of contents
- [About_this_App](#About_this_App)
- [Get_Started](#Get_Started)
- [Books_App](#Books_App)
  * [models](#models)
  * [migrations](#migrations)
  * [admin](#admin)
  * [server](#server)
  * [views](#views)
  * [urls](#urls)
  * [templates](#templates)
  * [logins](#logins)
- [Accounts_App](#Accounts_App)
  * [signup](#signup)
  * [signup_view](#signup_view)
  * [static_files](#static_files)
- [Paypal_payment_process](#Paypal_Payment_Process)
- [Running project via docker](#Run_via_Docker)
  
<hr>

## About_this_App
A Beautifully designed Online Bookstore which contains multiple Books, the site allows you to search your favourite book in the bookstore, i didnt added too many book in database for now, but you can customize the site the way you like with the help of the source code present in this repository. You can purchase any book you like by two payment methods the first option is of paypal and the other one is debit card, use the sandbox paypal account please :)

Also, before purchasing any book you will be redirected to the login or signup page. So that new users can signup on the site and then can buy their favourite book. The site also informs which book is available and which one is out of stock !.

## Get_Started

I'm assuming that you are already done with setting up virtual enviornment in your system. Ok, now lets move to a location where we can store this project by using terminal or command prompt in windows. In my case im at this location,

yash@yash-SVE15113ENB:~/Documents/django_project/$ 

* Now Setup the virtual environment

$`pipenv shell`

$`pipenv install django==3.0`

## Books_App

Lets begin our project by starting our project and installing a books app, type below commands in terminal.

(django_project)$`django-admin startproject ecom_project .` (do not avoid this period)

(django_project)$`python manage.py startapp books`

Now, open your favourite IDE and locate this project directory. (Im using VS Code so it should be something like this) note that at this point django doesnt know about this app, therefore we need to mention this app name inside our settings.py file.

* settings.py 

open your ecom_project folder, in here you will find settings.py file (open it). Go to Installed app section and mention your app name there (as shown below).


	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',

	    # my apps,				# changes
	    'books.apps.BooksConfig',
	    ]


### models

When done with the settings.py file, open the books folder (our app), in here you we find models.py file (open it)
Now put the following code in it,


	from django.db import models
	from django.urls import reverse

	class Book(models.Model):
	    title  = models.CharField(max_length = 200)
	    author = models.CharField(max_length = 200)
	    description = models.CharField(max_length = 500, default=None)
	    price = models.FloatField(null=True, blank=True)
	    image_url = models.CharField(max_length = 2083, default=False)
	    follow_author = models.CharField(max_length=2083, blank=True)  
	    book_available = models.BooleanField(default=False)

	    def __str__(self):
		return self.title


	class Order(models.Model):
		product = models.ForeignKey(Book, max_length=200, null=True, blank=True, on_delete = models.SET_NULL)
		created =  models.DateTimeField(auto_now_add=True) 

		def __str__(self):
			return self.product.title


* what we done here ?

I created a model named as 'Book' working on default django model (models.Model), this model contains 7 fields. Why ? beacuse when we buy a book the thing which commonly occurs in our mind are, the book's name, author and price tag. To make our website more informative i set a description field which gives short description about the book, an image of book so that buyer can easily recognize their book, some author reference and at last the most important thing, is the book available in stock or not. For that i used boolean field in book_available category. This allows the admin to update the bookstore as per the availability of books. By setting it to True (book is available) or False (out of stock).

Next model is our 'Order' model which basically takes the record ordered books. It has one product field which has a ForeignKey relationship (more on <a href = "https://docs.djangoproject.com/en/3.0/topics/db/examples/one_to_one/">ForeignKey</a>) with our Book model
and the other field is created which takes a record of at which time order is being made.

Also, both models uses a def__str__(self) for title, which is basically a string representation which means that on admin page for both models the book title will be shown up instead of the some id like ---> object.id(1) which is not that friendly to understand.

Note: max_length is used to ensure that only certain limit of characters is being used in the field (in the case of title and author the admin can use up to 200 characters only and in description upto 500 characters). You can change these values if you like. The next thing is default=False, any field which uses this condition means, that particular field cannot be empty and must be filled by the user.  

## migrations 

now its time to create some tables in our database, most of which is already handled by django, we just need to run following commands:

(django_project)$`python manage.py makemigrations`

(django_project)$`python manage.py migrate`

simply, the migrations command tells us what changes are going to be made in our database (right now two models will be created one is Book and other one is Order), the migrate command is just like conformation stage of makemigrations command (means if you agree with the changes mentioned by migrations command then in order to perform those changes we run migrate command) 

Note: its a quick illustration of these commands the depth knowledge is available in <a href="https://docs.djangoproject.com/en/3.0/topics/migrations/">django documentation</a>


### admin

now we need to register our models in admin file in order in to use them. Put the following code in admin.py file

	from django.contrib import admin
	from .models import Book, Order

	admin.site.register(Book)
	admin.site.register(Order)


Here, .models means from this current directory import the Book and Order model, from Models.py file and
for each model to register we need the command --> admin.site.register(model_name)

### server

Now, lets check that our model is being registered properly or not. First lets ensure that our server is running properly. Put the following commmand in terminal:

(django_project)$`python manage.py runserver`

* now open this link in your browser http://127.0.0.1:8000/

You will see a rocket there and a message saying, 'The install worked successfully! Congratulations!'

if yes, we didn't make any mistakes. Good !

* Now go to admin page by using this link http://127.0.0.1:8000/admin/

Just below users you will see our books app containing our models Books and Orders (we named the models as Book and Order the extra 's' in the end of model name is generated by django automatically). Click on Books model it will land us on a page saying 'Select a book to change', in the right corner there is a button saying 'ADD BOOK +'. click on this button, now you will see a page containg all the field of our Book model fill all the fields. 

Note: to fill image_url go to google and select any image now right click that image and choose the option 'copy image address' click on it and paste that inside image_url filed. A tick mark on the Book Available field means book is available and uncheck means book is not available or out of stock. After filling all the fields click on save button (at bottom right). You will see your created book name now. Create few more books if you like (atleast have 3).


### views

Now lets see our books on our webpage but before that we need to work on views. In this case im gonna use 'Class Based Views' which makes our code as much DRY (Don't Repeat Yourself) as possible and faster to implement. Put the follwing code in your views.py file.


	from django.shortcuts import render 
	from django.views.generic import ListView, DetailView
	from django.views.generic.edit import CreateView
	from .models import Book, Order
	from django.urls import reverse_lazy
	from django.db.models import Q # for search method
	from django.http import JsonResponse
	import json



	class BooksListView(ListView):
	    model = Book
	    template_name = 'list.html'


	class BooksDetailView(DetailView):
	    model = Book
	    template_name = 'detail.html'


	class SearchResultsListView(ListView):
		model = Book
		template_name = 'search_results.html'

		def get_queryset(self): # new
			query = self.request.GET.get('q')
			return Book.objects.filter(
			Q(title__icontains=query) | Q(author__icontains=query)
			)

	class BookCheckoutView(DetailView):
	    model = Book
	    template_name = 'checkout.html'


	def paymentComplete(request):
		body = json.loads(request.body)
		print('BODY:', body)
		product = Book.objects.get(id=body['productId'])
		Order.objects.create(
			product=product
		)
		return JsonResponse('Payment completed!', safe=False)



Note: A lot of things is going on here, ill try keep things as simple as possible, again this guide is not for absolute beginners so im not going to cover core django concepts here but still ill give you some idea of whats being done here. Lets go step by step,

* The 'BookListView' is a class which basically using the django module ListView to output the contents of Our book model (as i choose model = Book) in a list manner and the template on which its working on is list.html.
  
* Similarly, the class 'BookDetailView' class using DetailView to output the contents of Our book model in a detailed manner and the template on which its working on is detail.html. 

* The class 'SearchResultsView' class using ListView which provides the search results in a list manner and the template on which its working on is search_results.html. The SearchResultsView will match the search input provided by the user with the book title and the author's name (means you can search a book by its name or by its author name).

* The 'BookCheckoutView' is a class using DetailView and the template on which its working on is checkout.html. So that user can confirm that they are paying for the right book.

* At last, we have a function called paymentComplete which basically keeps a record of which book is being purchased by the user and that record gets updated in our Order Model. The payment process can be completed in two ways, by using paypal or debit card.


### urls

Now to make our class based views work we need url routing. By default we have a single urls.py file in our ecom_project directory and not in books app. So lets create a urls.py file in our app (why so ? so that django can easily find which url is working for which app, therfore instead of putting all urls in a single file its better to create seperate urls.py file for each app). Inside your books app create a new urls.py file. (you can do it by using your IDE or by following below code)

for linux users

$touch books/urls.py


Before putting some code in this file go to ecom_project folder and open urls.py file. Update this file in the follwing manner

	from django.contrib import admin
	from django.urls import path, include # changes

	urlpatterns = [
	    path('admin/', admin.site.urls),
	    path('', include('books.urls')),  # changes
	]

In short, here im telling django that im using a seperate urls.py file for my books app. Now go back to our app level url.py file (or open the urls.py file of our books app). Put the following code there


	from django.urls import path
	from .views import BooksListView, BooksDetailView, BookCheckoutView, paymentComplete, SearchResultsListView


	urlpatterns = [
	    path('', BooksListView.as_view(), name = 'list'),
	    path('<int:pk>/', BooksDetailView.as_view(), name = 'detail'),
	    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
	    path('complete/', paymentComplete, name = 'complete'),
	    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
	]


* what we done here ? 

At first i imported 'path' module from django.url library which we will use for url routing, then i imported all the class based views here which we created in views.py file, then in urlpatterns section im telling django at which location or url which webpage should work.

For BookListView.as_view() i used empty quotation marks -> ''  what it does ? it tells django that on the very first page work as per the BookListView class and then i choose a reference name for this url as 'list' and mentioned it inside name.

Next is BookDetailView which will be loaded after the BookListView class. The 'int' in int:pk denotes an integer and the pk denotes primary key. If you remember we created some books on our admin page and when saved it, that book automatically gets an id=1 by default, similary the id for the next books gets incremented by +1 which means the second book gets an id of 2 (id=2) and for third book (id=3) and so on.

Also, the BookDetailView uses this <int:pk> or id to show the details of a particular book. Means, if id '1' is requested we will see details of first book, when id=2 then we get details of second book and so on. The BookCheckout will work after this detail page which shows which book is going to be purchased by user and the last two urls are working seperately.


### templates

Its time for templates now, if you remember we used template_name in our class based views. The content on the webpage basically comes from templates (actually html files) and the views holds the overall functionality in short. First lets create a template folder, your templates folder should be outside your ecom_project folder, forex: take a look at my <a href = "https://github.com/YashMarmat/django-ecommece-bookstore">repository</a>. Mean place the folder just below the ecom_project folder (note: there are many ways to use templates in django but for now im using this approach).

* or just follow below command

(django_project)$`mkdir templates`

now open your settings.py file from ecom_project folder and update the Template section in the following manner.

	TEMPLATES = [
	    {
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],			# changes
		'APP_DIRS': True,
		'OPTIONS': {
		    'context_processors': [
			'django.template.context_processors.debug',
			'django.template.context_processors.request',
			'django.contrib.auth.context_processors.auth',
			'django.contrib.messages.context_processors.messages',
		    ],
		},
	    },
	]

Inside templates folder create 5 .html files namely --> base.html, checkout.html, detail.html, list.html, search_results.html (again order doesn't matter). Update the files by putting the codes mention in below links

<a href ="https://github.com/YashMarmat/django-ecommece-bookstore/blob/master/templates/base.html">base.html</a>, <a href ="https://github.com/YashMarmat/django-ecommece-bookstore/blob/master/templates/checkout.html">checkout.html</a>, <a href ="https://github.com/YashMarmat/django-ecommece-bookstore/blob/master/templates/detail.html">detail.html</a>, <a href ="https://github.com/YashMarmat/django-ecommece-bookstore/blob/master/templates/list.html">list.html</a>, <a href ="https://github.com/YashMarmat/django-ecommece-bookstore/blob/master/templates/search_results.html">search_results.html</a>

Note: detail knowledge of templates is not given here as i said earlier im assuming that you have the basic knowlege of MVT in django.

* base.html contains the navigation bar for our website taken form bootstrap.
* list.html provides listing of all the books (created on admin page).
* detail.html provides details like book title, author name, description and detail of all the fields present in our Book model.
* checkout.html provides the detail of which book you selected for purchase and provides you two option of payment --> paypal and debit card.
* search_results provides you the search results by matching the user input (provided in search bar) with the book title and author name.

### logins


At this point anyone can buy books from our online bookstore without creating an account on out website. So we going to restrict that by using a Mixin in django called LoginRequiredMixin. Update your BookCheckoutView class present in views.py file of books app. Code below, 

	from django.contrib.auth.mixins import LoginRequiredMixin 

	class BookCheckoutView(LoginRequiredMixin, DetailView):
	    model = Book
	    template_name = 'checkout.html'
	    login_url     = 'login'

Now this class is working on 'LoginRequiredMixin' it basically makes sure that before visiting the checkout page the user must login (means the user needs to have an account on our website before purchasing any books, if the user is not logged in then the user will be redirected to page which contains two options --> Log In and Sign Up). More on Signup in short.

now to make login work go to the urls.py file of ecom_project and open it. Update the code as shown below,

	from django.contrib import admin
	from django.urls import path, include

	urlpatterns = [
	    path('admin/', admin.site.urls),
	    path('', include('books.urls')),
	    path('accounts/', include("django.contrib.auth.urls")),   # changes
	]

Note: we do not require to create a seperate class based view or function based view, all that will be handled by 'django.contrib.auth.urls'
provided by django. But we do require a template file for it. Now login template needs to created in a specific way. As illustrated below,


* inside tempaltes folder create another folder called 'registration'
* now inside this registration folder create template file and name it --> login.html


Now update the login.html file from <a href="https://github.com/YashMarmat/django-ecommece-bookstore/blob/master/templates/registration/login.html">here</a> 

ok, a little more work on logins, by default django doesnt know where to send the user after they log in and after they log out. So we need to use the url reference name (created in urls.py file of books app). So, i want that after the user logs in and logs out that user should be sent to the home page or the very first page of our website and the url working working on that page was 'list'. Remember those empty quotation marks?  see below:

no updation just for illustation !

	urlpatterns = [
	    path('', BooksListView.as_view(), name = 'list'),  # the home page or list page
	    path('<int:pk>/', BooksDetailView.as_view(), name = 'detail'),
	    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
	    path('complete/', paymentComplete, name = 'complete'),
	    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
	] 


Now to make this work open the setting.py file (present inside the ecom_project folder). Put the below codes at the bottom of the file.


	LOGIN_REDIRECT_URL = 'list'   # controls login
	LOGOUT_REDIRECT_URL = 'list'  # controls logout


Thats it! login is done. (next signup)


## Accounts_App


### signup

Lets think about login again, a user can login only if they have an account on our site right ? so we need to provide a sign up page as well where users can create their account and then can log in successfully. Lets create a seperate app which will handle all the signup process. Just making code easier to read. Follow below command:

(django_project)$`python manage.py startapp accounts`

To let django know about this app lets update settings.py file (inside ecom_project). Update the file in following manner

	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',

	    # my apps,
	    'books.apps.BooksConfig',
	    'accounts.apps.AccountsConfig',  # changes
	]


### signup_view


now we will create a new class called SignUpView which will handle the sign up page. Put below code in signup.html file

	from django.urls import reverse_lazy
	from django.contrib.auth.forms import UserCreationForm
	from django.views import generic


	class SignUpView(generic.CreateView):
	    form_class    = UserCreationForm
	    success_url   = reverse_lazy('login')
	    template_name = 'signup.html'


* what we done here ?

at first i imported reverse_lazy a module which takes a url name, the url metioned in reverse lazy basically loads that url page when user is done with the current page. Means when the user fills the signup page successfully he will be redirected to the login page. see this line of code -->  success_url = reverse_lazy('login') in above class.

the UserCreationForm is a form provided by django which contains all the neccessary fields required for a signup page. Means we don't need to create a signup page by our own and in the last it will load the content present in the template file mentioned in this class.


* now time for signup.html template 

go to templates folder and create a signup.html file (Note: do not put signup.html file inside registration folder, by doing that django will throw tempate does not exist Error). Follow below code,


(django_project)$`touch templates/signup.html`


put the code in signup.html, present <a href = "https://github.com/YashMarmat/django-ecommece-bookstore/blob/master/templates/signup.html">here</a>.


ok, we done with the views now its time for url routing, go ahead and create a new urls.py for this accounts app.

(django_project)$`touch accounts/urls.py`

put the below code in this file

	from django.urls import path
	from .views import SignUpView

	urlpatterns = [
	    path('accounts/', SignUpView.as_view(), name = 'signup'),
	]


Now, as we did earlier we let django know we are using a seperate urls.py file for our accounts app. Update the urls.py file of ecom_project in the following manner,


	from django.contrib import admin
	from django.urls import path, include

	urlpatterns = [
	    path('admin/', admin.site.urls),
	    path('', include('books.urls')),
	    path('', include("accounts.urls")),  # changes
	    path('accounts/', include("django.contrib.auth.urls")),   # working for logins
	]



signup process is completed !


### static_files

In short, a static file basically takes care of all the css, javasript and Images present in our project. I used a lot of css in my search bar if you noticed by visting my bookstore site. Providing you detail knowledge of it is not the scope of this guide, but dont worry its not that complicated to understand if you have even basic knowledge of CSS :)

I also used some javasript in my chekout.html file but again providing the detail knowledge of it is not the scope of this guide, but if you have the basic knowledge javascript you will get it.

Ok, to use some static css in django we need to update few thing in our settings.py, open it and put the code at bottom of the file. 

	STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # requires collectstatic command
	STATIC_URL = '/static/'
	STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


	# (optional)
	STATICFILES_FINDERS = [
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder",
	]


* now create a static folder and place it outside the ecom_project folder. Then inside this static folder create another folder called 'css' then inside this css folder create a file called base.css (follow below code).

(django_project)$`mkdir static`

(django_project)$`mkdir static/css`

(django_project)$`touch static/css/base.css`

open 'base.css' folder and put this <a href="https://github.com/YashMarmat/django-ecommece-bookstore/blob/master/static/css/base.css">code</a> in it.

Now, save everything and test your bookstore website :)

(django_project)$ python manage.py runserver


All Done! :)

if you ran into some issues at some point please let me know. Go to issues section of this repository put your problems there. I'll answer them as soon as possible or email me for any feedback --> yashmarmat08@gmail.com

### Paypal_payment_process
https://scribehow.com/shared/How_to_complete_a_purchase_on_a_website__ereaJRxxQeSAuI-LS1zLbA

### Run_via_Docker

`docker compose up --build` (to build and start the docker container)

`docker compose down` (to stop and remove the docker container)

<p><a href="#top">Back to Top</a></p>
