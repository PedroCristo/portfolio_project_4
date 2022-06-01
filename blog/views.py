from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from posts.models import *
from .forms import CommentForm



def index(request):
    """View to return the index page"""
    queryset = Post.objects.filter(featured=True
    ).order_by('-timestamp')
    categories = Category.objects.all()

    context = {
        'post_list': queryset,
        'categories_list': categories,
    }
    
    return render(request, 'index.html', context)


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-timestamp")
        num_comments = Comment.objects.filter(post=post).count()
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
                'num_comments': num_comments,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-timestamp")
        liked = False

        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        comment_form = CommentForm(data=request.POST)
        if  comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked,
            },
        )  


def about(request):
    """View to return the about page"""
    categories = Category.objects.all()
    context = {
        'categories_list': categories
    }
    return render(request, 'about.html', context)          