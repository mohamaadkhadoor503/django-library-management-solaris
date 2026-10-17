from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Author, Book, Category


def _library_stats() -> dict[str, int]:
    """Return headline counts shown on the home page and dashboard."""
    return {
        "total_books": Book.objects.count(),
        "total_authors": Author.objects.count(),
        "total_categories": Category.objects.count(),
    }


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Render the library home page.
    """
    context = {
        **_library_stats(),
        "latest_books": Book.objects.select_related("author").order_by("-pk")[:3],
    }

    return render(request, "home.html", context)


def books_view(request: HttpRequest) -> HttpResponse:
    """
    Display all books stored in the database.
    """
    books = Book.objects.select_related("author").prefetch_related("categories")

    context = {
        "books": books,
        "categories": Category.objects.all(),
    }

    return render(request, "books.html", context)


def book_detail_view(
    request: HttpRequest,
    book_id: int,
) -> HttpResponse:
    """Display details for a specific book."""

    book = get_object_or_404(
        Book.objects.select_related("author").prefetch_related("categories"),
        pk=book_id,
    )

    context = {
        "book": book,
        "related_books": book.author.books.exclude(pk=book.pk)[:3],
    }

    return render(request, "book_detail.html", context)


def dashboard_view(request: HttpRequest) -> HttpResponse:
    """Display library statistics and book overview."""

    stats = _library_stats()
    categories = Category.objects.annotate(book_count=Count("books")).order_by(
        "-book_count", "name"
    )
    for category in categories:
        category.share = (
            round(category.book_count * 100 / stats["total_books"])
            if stats["total_books"]
            else 0
        )

    context = {
        **stats,
        "books": Book.objects.select_related("author"),
        "categories": categories,
    }

    return render(request, "dashboard.html", context)
