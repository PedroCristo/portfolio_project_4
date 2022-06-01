from posts.models import Comment, Profile
from django.contrib.auth.models import User
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)