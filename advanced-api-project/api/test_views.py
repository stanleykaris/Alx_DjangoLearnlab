from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author
from rest_framework.permissions import IsAuthenticated

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.author = Author.objects.create(name='Test Author')
        self.book_data = {
            'title': 'Test Book',
            'author': self.author,
            'publication_year': 2024
        }
        self.book = Book.objects.create(**self.book_data)
        self.url_list = '/api/books'
        self.url_detail = f'/api/books/{self.book.id}'
        self.client.login(username='testuser', password='password')
        
    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2024
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['author'], data['author'])
        self.assertEqual(response.data['publication_year'], data['publication_year'])
        
    def test_retrieve_books(self):
        response = self.client.get(self.url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Ensure at least one book is returned
        
    def test_retrieve_single_book(self):
        response = self.client.get(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)
        
    def test_update_book(self):
        updated_author = Author.objects.create(name='Updated Author')
        data = {
            'title': 'Updated Book',
            'author': updated_author.id,
            'publication_year': 2025
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, data['title'])
        self.assertEqual(self.book.author, data['author'])
        self.assertEqual(self.book.publication_year, data['publication_year'])
    
    def test_delete_book(self):
        response = self.client.delete(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensuring that the book is deleted from the database
        self.assertEqual(Book.objects.count(), 0)
        
    def test_permissions_for_create(self):
        self.client.logout()
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2024
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_search_books(self):
        response = self.client.get(self.url_list, {'search': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0) # Ensure book match search query.
        
    def test_filter_books(self):
        response = self.client.get(self.url_list, {'author': 'Test Author'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Ensure book match filter criteria.
        
    def test_ordering_books(self):
        response = self.client.get(self.url_list, {'ordering': 'title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]['title'] <= response.data[-1]['title'])