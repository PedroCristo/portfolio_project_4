from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Book
from .forms import BookForm
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def books(request):
    """
    Renders the books page
    """
    books_list = Book.objects.all().filter(
        approved=True).order_by("-timestamp")
    return render(request, 'books/books.html', {'books_list': books_list})


class AddBook(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Add Book
    """
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_message = """Your post was sent successfully <br>
    and is awaiting approval!"""

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)


class EditBook(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit Book
    """
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_message = 'The post was successfully updated'


def delete_book(request, book_id):
    """
    Delete Book
    """
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'The post was deleted successfully')
    return redirect('books')
