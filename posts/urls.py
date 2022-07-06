from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .forms import CommentForm

from .views import *

"""url paths"""
urlpatterns = [
    path('delete_comment/<int:comment_id>', views.delete_comment,
         name='delete_comment'),
    path('edit_comment/<int:pk>', views.EditComment.as_view(),
         name='edit_comment'),
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('about/', views.about, name="about"),
    path('blog/', views.BlogPost.as_view(), name="blog"),
    path('contact/', views.contact, name="contact"),
    path('categories/', views.categories, name="categories"),
    path('categories_posts/<str:cats>', views.categories_view,
         name="categories_posts"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('profile', views.profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
