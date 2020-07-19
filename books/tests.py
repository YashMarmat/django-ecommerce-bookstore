from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Book


class BookTest(TestCase):

    def setUp(self): # filling user data (credentials)
        self.user = get_user_model().objects.create_user(
            username = 'yash',
            email = 'yashmarmat08@gmail.com',
            password = 'secret',
        )

        self.book = Book.objects.create(    # filling Book model fields
            title = 'django for beginners',
            author = 'WS Vincent',
            description = 'anything',
            price = '30',
            image_url = 'https://forexample.jpg',
            follow_author = 'https://twitter.com/wsv3000?lang=en',
            book_available = 'True',
        )

    def test_string_representation(self):
        book = Book(title='new book')
        self.assertEqual(str(book), book.title)

    def test_book_model_fields_content(self):
        self.assertEqual(f'{self.book.title}', 'django for beginners')
        self.assertEqual(f'{self.book.author}', 'WS Vincent')
        self.assertEqual(f'{self.book.description}', 'anything')
        self.assertEqual(f'{self.book.price}', '30')
        self.assertEqual(f'{self.book.image_url}', 'https://forexample.jpg')
        self.assertEqual(f'{self.book.follow_author}', 'https://twitter.com/wsv3000?lang=en')
        self.assertEqual(f'{self.book.book_available}', 'True')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(username = 'yash', email='yashmarmat08@gmail.com', password='secret')
        request = self.client.get(reverse('list'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_book_list_view_for_anonymous_user(self): # a user who doesn't have an account on our site
        self.client.logout()
        request = self.client.get(reverse('list'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_book_detail_view_for_logged_in_user(self):
        self.client.login(username = 'yash', email='yashmarmat08@gmail.com', password='secret')
        request = self.client.get(reverse('detail', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, 'WS Vincent')
        self.assertContains(request, '30')

    def test_book_detail_view_for_anonymous_user(self):
        self.client.logout()
        request = self.client.get(reverse('detail', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, 'WS Vincent')
        self.assertContains(request, '30')

    def test_checkout_view_for_logged_in_user(self):
        self.client.login(username = 'yash', email='yashmarmat08@gmail.com', password='secret')
        request = self.client.get(reverse('checkout', args='1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'django for beginners')
        self.assertContains(request, '30')

    def test_checkout_view_for_anonymous_user(self):
        self.client.logout()
        request = self.client.get(reverse('checkout', args='1'))
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, '/accounts/login/?next=/1/checkout/') # redirects the user to login page

    def test_book_when_available(self):  # a second book is created (out of stock)
        request = self.client.get(reverse('detail', args = '1'))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'Buy Now') 
        self.assertNotContains(request, 'Out of Stock !') # should not be there
        
    def test_book_when_out_of_stock(self):  # a second book is created which is out of stock
            book = Book.objects.create(
                title = 'new book',
                author = 'yash',
                description = 'anything',
                price = '30',
                image_url = 'https://forexample.jpg',
                follow_author = 'https://twitter.com/wsv3000?lang=en',
                book_available = 'False',   # out of stock when False
            )
            request = self.client.get(reverse('detail', args = '2'))
            self.assertEqual(request.status_code, 200)
            self.assertContains(request, 'Out of Stock !')
            self.assertNotContains(request, 'Buy Now') # buy now option is no longer present
            