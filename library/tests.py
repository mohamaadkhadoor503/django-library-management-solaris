from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, Category


class ModelTests(TestCase):
    """Tests for library models."""

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name="Ali", email="ali@example.com")
        cls.category = Category.objects.create(name="Programming")
        cls.book = Book.objects.create(title="Django Basics", author=cls.author)
        cls.book.categories.add(cls.category)

    def test_str_methods(self):
        self.assertEqual(str(self.author), "Ali")
        self.assertEqual(str(self.category), "Programming")
        self.assertEqual(str(self.book), "Django Basics")

    def test_published_date_is_optional(self):
        self.assertIsNone(self.book.published_date)

    def test_author_has_many_books(self):
        Book.objects.create(title="Advanced Django", author=self.author)

        self.assertEqual(self.author.books.count(), 2)

    def test_book_has_many_categories(self):
        web = Category.objects.create(name="Web")
        self.book.categories.add(web)

        self.assertEqual(self.book.categories.count(), 2)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.book.get_absolute_url(),
            reverse("book_detail", args=[self.book.pk]),
        )


class LibraryViewTests(TestCase):
    """Tests for library pages."""

    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(name="Sara", email="sara@example.com")
        category = Category.objects.create(name="Web Development")
        cls.book = Book.objects.create(
            title="Python Web Development",
            description="Building websites with Python.",
            published_date=date(2025, 1, 15),
            author=author,
        )
        cls.book.categories.add(category)

    def test_home_page(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_books_page(self):
        response = self.client.get(reverse("books"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "books.html")
        self.assertEqual(len(response.context["books"]), 1)
        self.assertContains(response, "Python Web Development")
        self.assertContains(response, "Sara")
        self.assertContains(response, "Web Development")

    def test_books_page_empty(self):
        Book.objects.all().delete()

        response = self.client.get(reverse("books"))

        self.assertContains(response, "No books available.")

    def test_book_detail_page(self):
        url = reverse("book_detail", args=[self.book.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_detail.html")
        self.assertContains(response, "Python Web Development")
        self.assertContains(response, "Building websites with Python.")
        self.assertContains(response, "Sara")
        self.assertContains(response, "Web Development")

    def test_nonexistent_book_detail(self):
        url = reverse("book_detail", args=[9999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_unknown_url_uses_custom_404_page(self):
        response = self.client.get("/this-page-does-not-exist/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "missing from our shelves", status_code=404)

    def test_dashboard_page(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")
        self.assertEqual(response.context["total_books"], 1)
