from django.contrib import admin
from .models import Author, Category, Post, Comment, Profile
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Add fields for Author in admin panel
    """
    list_display = ('user', 'timestamp')
    search_fields = ['user']


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Add fields which will use summernote editor in admin panel
    """
    list_display = (
                   'title', 'slug', 'status', 'timestamp', 'author', 'featured'
                   )
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Add fields for comments in admin panel
    """
    list_display = ('name', 'body', 'post', 'timestamp', 'approved')
    list_filter = ('approved', 'timestamp')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Add fields for the profile in the admin panel
    """
    list_display = ('user',)
