from django.contrib import admin

from .models import Author, Book, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    list_filter = ("categories", "author")
    search_fields = ("title", "author__name")
    list_select_related = ("author",)
    autocomplete_fields = ("author",)
    filter_horizontal = ("categories",)
