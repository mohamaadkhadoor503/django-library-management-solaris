from django.db import models
from django.urls import reverse


class Author(models.Model):
    """A person who writes books."""

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """A genre or topic used to group books."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """A book in the library, written by one author."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )
    categories = models.ManyToManyField(
        Category,
        related_name="books",
        blank=True,
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("book_detail", args=[self.pk])
