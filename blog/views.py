from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse, redirect, resolve_url
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


class PostLike(View):
    """View for post like/Unlike"""
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))         


def about(request):
    """View to return the about page"""
    categories = Category.objects.all()
    context = {
        'categories_list': categories
    }
    return render(request, 'about.html', context)   


class BlogPost(generic.ListView):
    """View to return the blog page"""
    model = Post
    template_name = 'blog.html'
    paginate_by = 3
    extra_context={'categories_list': Category.objects.all()}    


def contact(request):
    """View to return the contact page"""
    categories = Category.objects.all()
    context = {
        
            'categories_list': categories
    }
        
    return render(request, 'contact.html', context)


def categories(request):
    """View to return the categories page"""
    categories = Category.objects.all()
    context = {
        'categories_list': categories
    }
    return render(request, 'categories.html', context)   


def CategoriesView(request, cats): 
    """View to return the posts filtered by categories""" 
    categories_posts = Post.objects.filter(categories__title__contains=cats)
    return render(request, 'categories_posts.html', {
        'cats':cats.title(), 'categories_posts':categories_posts })
        
         
def search(request):
    """search results"""
    queryset = Post.objects.all()
    if request.method == "POST":
        searched = request.POST["searched"]
        results = Post.objects.filter(
                Q(title__contains=searched) |
                Q(overview__icontains=searched) |
                Q(content__icontains=searched) 
            ).distinct()
        context = {
        'queryset': queryset
        }

        return render(request, 'search.html', {
            'results': results, 'searched': searched})
    else:

        return render(request, 'search.html', context)
