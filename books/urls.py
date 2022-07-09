from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


"""url paths"""
urlpatterns = [
    path('books', views.books, name='books'),
    path('add_book/', views.AddBook.as_view(), name='add_book'),
    path('edit_book/<int:pk>', views.EditBook.as_view(), name='edit_book'),
    path('delete_book/<int:book_id>', views.delete_book, name='delete_book'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)