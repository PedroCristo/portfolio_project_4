"""tastyblog URL Configuration"""


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls'), name='blog.urls'),
    path('summernote/', include('django_summernote.urls')),
]
