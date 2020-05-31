# Django-Ecommece-Bookstore
An online bookshop developed in django-3 which allow users to purchase books online :) 

This guide will Step-by-Step help you to create your own ecommerce bookstore application in django. With only HTML, CSS, JAVASCRIPT and yeah our Django Framework. 

Note: this guide is not for absolute beginners so im assuming you have the basic knowledge of MVT in django to get started. To know more on it
i recommed you django documentation.

# Table of contents
- [About_this_App](#About_this_App)
- [Get_Started](#Get_Started)
- [Books_app](#Books_app)
- [models](#models)
- [migrations](#migrations)
- [admin](#admin)
- [views](#views)


## About_this_App
A Beautifully designed Online Bookstore which contains multiple Books, the site allows you to search your favourite book in the bookstore, i didnt added too many book in database for now, but you can customize the site the way you like with the help of the source code present in this repository. You can purchase any book you by two payment methods the first option is of paypal and the other one is debit card, use the fake one please :)

Also, before purchasing any book you will be redirected to the login or signup page. So that new users can signup on the site and then can buy their favourite book. The site also informs users which book is available and which one is out of stock !.


* checkout the site here: https://ym-djecom.herokuapp.com

## Get_Started

I'm assuming that you are already done with setting up virtual enviornment in your system. 
Ok, now lets move to a location where we can store this project by using terminal or command prompt in windows.
In my case im at this location

yash@yash-SVE15113ENB:~/Documents/django_project/$ 

## Books_app

Lets begin our project by starting our project and installing a books app, type below commands in terminal.

$`django-admin startproject ecom_project .` (do not avoid this period)

$`python manage.py startapp books`

Now, open your favourite IDE and locate this project directory. (Im using VS Code so it should be something like this)

Note: at this point django doesnt know about this app, therefore we need to mention this app name inside our settings.py file.

* setting.py 

open your ecom_project folder, in here you will find settings.py file (open it)
Go to Installed app section and mention your app name there (as shown below)


## models

when done with the settings.py file, open the books folder (our app), in here you we find models.py file (open it)
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

I created a model named as 'Book' working on default django model (models.Model)
this model contains 7 fields. Why ? beacuse when we buy a book the thing which commonly occurs in our mind are,
the book's name, author and price tag. To make our website more informative i set a description field which gives short description 
about the book, an image of book so that buyer can easily recognize their book, some author reference and at last 
the most important thing is the book available in stock or not. For that i used boolean field in book_available category.
This allows the admin to update the bookstore as per the availability of books. By setting it to True (book is available) or 
False (out of stock).

next model is our 'Order' model which basically takes the record of the which book is ordered. It has one product field which 
has a ForeignKey relationship (to know more about ForeignKey i recommend you to look in django documentation) with our Book model
and the other field is created which takes a record of at which time is order is being made.

Also, both models uses a def__str__(self) for title which means that on admin page for both models the book title will be shown up
instead of the some id like ---> object.id(1) which is not that friendly to understand.

Note: max_length is used to ensure that only certain limit of characters is being used in the field (in the case of title and author 
the admin can use up to 200 characters only and in description upto 500 characters). You can change these values if you like. The 
next thing is default=False, any field which uses this condition means, that particular field cannot be empty and it must be filled.  

## migrations 

now its time to create some tables in our database, most of which is already handled by django, we just need to run following commands

$`python manage.py makemigrations`

$`python manage.py migrate`

simply, the migrations command tells us what changes are going to be made in our database (right now two models will be created one is Book
and other one is Order)
the migrate command is just like conformation stage of makemigrations command (means if you agree with the changes mentioned by migrations 
command then in order to perform those changes we run migrate command) 

Note: its a quick illustration of these commands the depth knowledge is available in documentation


## admin

now we need to register our models in admin file in order in to use them. Put the following code in admin.py file

from django.contrib import admin
from .models import Book, Order


$`admin.site.register(Book)`

$`admin.site.register(Order)`


Here, .models means from this current directory import the Book and Order model, from Models.py file and
for each model to register we need the command --> admin.site.register(model_name)


Now lets check that our model is being registered properly or not. First lets ensure that our server is running properly. Put the following
commmand in terminal one by one:

python manage.py runserver

now open this link in your browser http://127.0.0.1:8000/

you will see a rocket there and a message saying The install worked successfully! Congratulation!

if yes, we didn't make any mistakes. Good !

now go to admin page by using this link http://127.0.0.1:8000/admin/

just below users you will see our books app name containing our models Books and Orders (we named the models as Book and Order the 
extra 's' is generated by django automatically). Click on Books model it will land us on a page saying 'Select a book to change' in the 
right corner there is a button saying 'ADD BOOK +'. click on this button, now you will see a page containg all the field of our Book model
fill all the field. 

Note: to fill image_url go to google and select any image now right click that image and choose the option 'copy image address' click on it and now paste that inside image_url filed. A tick mark on the Book Available field means book is available and uncheck means book is not available
or out of stock. After filling all the fields click on save button (at bottom right). You will see your created book name now. Create few more books if you like (atleast have 3).


## views

now lets see our books on our webpage but before that we need to work on views. In this case im gonna use 'Class Based Views' which make our 
code as much DRY as possible and faster to implement. Put the follwing code in your views.py file.


	from django.shortcuts import render 
	from django.views.generic import ListView, DetailView
	from django.views.generic.edit import CreateView
	from django.contrib.auth.mixins import LoginRequiredMixin 
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

	class BookCheckoutView(LoginRequiredMixin, DetailView):
	    model = Book
	    template_name = 'checkout.html'
	    login_url     = 'login'


	def paymentComplete(request):
		body = json.loads(request.body)
		print('BODY:', body)
		product = Book.objects.get(id=body['productId'])
		Order.objects.create(
			product=product
		)
		return JsonResponse('Payment completed!', safe=False)



* Note: A lot of things is going on here, ill try keep things as simple as possible, again this guide is not for absolute beginners so im not going to cover core django concepts here but still ill give you some idea of whats being done here. Lets go step by step,

The 'BookListView' is a class which basically using the django module ListView to output the contents of Our book model (as i choose model = Book) in a list manner and the template on which its working on is list.html.
  
Similarly, the class 'BookDetailView' class using DetailView to output the contents of Our book model (as i choose model = Book) in a detailed manner and the template on which its working on is detail.html. 

The class 'SearchResultsView' class using ListView which provides the search results in a list manner and the template on which its working on is search_results.html. The SearchResultsView will match the search input provided by the user with the book title and the author's name
(means you can search a book by its name or by its author name).

The 'BookCheckoutView' is a class using DetailView and the template on which its working on is checkout.html. Now this class is working on 
'LoginRequiredMixin' it basically makes sure that before visiting the checkout page the user must be login (means the user needs to have an
account on our website before purchasing any books, if the user is not logged in then the user will be redirected to page which contains 
two options of Log In and Sign Up)

At last, we have a function called paymentComplete which basically keeps a record of which book is being purchased by the user and that record gets updated in our Order Model. The payment process can be completed in two ways, by using paypal or debit card.


## urls

  

 





























