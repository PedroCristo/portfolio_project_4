from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Add fields for Book in admin panel
    """
    list_display = ('name', 'title', 'timestamp', 'approved')
    list_filter = ('approved', 'timestamp')
    actions = ['approve_book']

    def approve_book(self, request, queryset):
        queryset.update(approved=True)
