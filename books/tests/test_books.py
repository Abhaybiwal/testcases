import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from books.models import Book
from datetime import date

@pytest.mark.django_db
def test_create_book():
    client = APIClient()
    url = reverse('book-list')
    data = {'title': 'Test Book', 'author': 'Author', 'published_date': '2023-01-01'}
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Book.objects.count() == 1

@pytest.mark.django_db
def test_get_books():
    Book.objects.create(title='B1', author='A1', published_date='2022-01-01')
    client = APIClient()
    url = reverse('book-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_get_single_book():
    book = Book.objects.create(title='B1', author='A1', published_date='2022-01-01')
    client = APIClient()
    url = reverse('book-detail', kwargs={'pk': book.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['title'] == 'B1'

@pytest.mark.django_db
def test_update_book():
    book = Book.objects.create(title='B1', author='A1', published_date='2022-01-01')
    client = APIClient()
    url = reverse('book-detail', kwargs={'pk': book.id})
    data = {'title': 'Updated', 'author': 'A2', 'published_date': '2022-01-01'}
    response = client.put(url, data, format='json')
    assert response.status_code == 200
    book.refresh_from_db()
    assert book.title == 'Updated'

@pytest.mark.django_db
def test_delete_book():
    book = Book.objects.create(title='B1', author='A1', published_date='2022-01-01')
    client = APIClient()
    url = reverse('book-detail', kwargs={'pk': book.id})
    response = client.delete(url)
    assert response.status_code == 204
    assert Book.objects.count() == 0

