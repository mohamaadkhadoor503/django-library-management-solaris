
from django.test import SimpleTestCase
from django.urls import reverse

from .services import get_all_books, get_book_by_id


class BookServiceTests(SimpleTestCase):
    """Tests for book-related services."""

    def test_get_all_books(self):
        books = get_all_books()

        self.assertEqual(len(books), 3)

    def test_get_existing_book(self):
        book = get_book_by_id(1)

        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "Django Basics")

    def test_get_nonexistent_book(self):
        book = get_book_by_id(99)

        self.assertIsNone(book)


class LibraryViewTests(SimpleTestCase):
    """Tests for library pages."""

    def test_home_page(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_books_page(self):
        response = self.client.get(reverse("books"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books.html")
        self.assertEqual(len(response.context["books"]), 3)

    def test_book_detail_page(self):
        url = reverse("book_detail", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_detail.html")
        self.assertContains(response, "Django Basics")

    def test_nonexistent_book_detail(self):
        url = reverse("book_detail", args=[99])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_dashboard_page(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")
        self.assertEqual(response.context["total_books"], 3)
