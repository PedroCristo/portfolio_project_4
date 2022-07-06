"""tastyblog URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls'), name='posts.urls'),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('allauth.urls')),
]