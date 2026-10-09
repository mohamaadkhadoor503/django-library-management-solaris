from typing import Optional, TypedDict

class Book(TypedDict):
    id: int
    title: str
    author: str
    year: int
    image: str


BOOKS: tuple[Book, ...] = (
    {
        "id": 1,
        "title": "Django Basics",
        "author": "Ali",
        "year": 2024,
        "image": "images/django_basics.png",

    },
    {
        "id": 2,
        "title": "Python Web Development",
        "author": "Sara",
        "year": 2025,
        "image": "images/python_web.png",

    },
    {
        "id": 3,
        "title": "Learning APIs",
        "author": "Omar",
        "year": 2023,
        "image": "images/learning_apis.png",

    },
)


def get_all_books() -> list[Book]:
    """Return all available library books."""
    return [book.copy() for book in BOOKS]

def get_book_by_id(book_id: int) -> Optional[Book]:
    """Find a book by its unique ID."""

    for book in BOOKS:
        if book["id"] == book_id:
            return book.copy()

    return None