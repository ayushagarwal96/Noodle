from django.contrib import admin
from books.models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher',)
    list_filter = ('author','publisher',)
    search_fields = ('title',)

admin.site.register(Book, BookAdmin)