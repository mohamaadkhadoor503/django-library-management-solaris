from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .services import get_all_books, get_book_by_id


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Render the library home page.
    """
    return render(request, "home.html")


def books_view(request: HttpRequest) -> HttpResponse:
    """
    Display all available library books.
    """
    context = {
        "books": get_all_books(),
    }

    return render(request, "books.html", context)

def book_detail_view(
    request: HttpRequest,
    book_id: int,
) -> HttpResponse:
    """Display details for a specific book."""

    book = get_book_by_id(book_id)

    if book is None:
        raise Http404("Book not found.")

    context = {
        "book": book,
    }

    return render(request, "book_detail.html", context)


def dashboard_view(request: HttpRequest) -> HttpResponse:
    """Display library statistics and book overview."""

    books = get_all_books()

    context = {
        "total_books": len(books),
        "books": books,
    }

    return render(request, "dashboard.html", context)
