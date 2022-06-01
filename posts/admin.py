from django.contrib import admin
from .models import Author, Category, Post
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Add fields for Author in admin panel
    """
    list_display = ('author', 'timestamp')
    search_fields = ['author']  


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Add fields which will use summernote editor in admin panel
    """
    list_display = ('title', 'slug', 'status', 'timestamp', 'author',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'timestamp')
    summernote_fields = ('content')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Add fields for Category in admin panel
    """
    list_display = ['title']
    search_fields = ['title']    