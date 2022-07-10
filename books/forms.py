from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for Book
    """
    class Meta:
        model = Book
        fields = ('picture', 'title', 'author', 'link', 'review')
