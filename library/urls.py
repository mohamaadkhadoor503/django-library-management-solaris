from django.urls import path

from . import views


urlpatterns = [
    path("", views.home_view, name="home"),
    path("books/", views.books_view, name="books"),
    path(
        "books/<int:book_id>/",
        views.book_detail_view,
        name="book_detail",
    ),
    path(
        "dashboard/",
        views.dashboard_view,
        name="dashboard",
    ),
]