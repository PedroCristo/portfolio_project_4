from django.views import generic, View
from django.contrib import messages
from posts.models import *
from .forms import CommentForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import(
    render, get_object_or_404, reverse, redirect, resolve_url)
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """Renders the index page"""
    queryset = Post.objects.filter(
        featured=True, status=1).order_by('-timestamp')
    context = {
        'post_list': queryset,
    }
    return render(request, 'index.html', context)


def about(request):
    """Renders the about page"""
    return render(request, 'about.html')


def contact(request):
    """Renders the contact page"""
    return render(request, 'contact.html')


def categories(request):
    """Renders the categories page"""
    return render(request, 'categories.html')


class PostDetail(View):
    """Renders the post detail Page"""
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
        """Comment on the posts"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-timestamp")
        liked = False

        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, f"""
            Your comment was sent successfully and is awaiting approval!""")
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


class PostLike(LoginRequiredMixin, View):
    """Like/Unlike posts"""
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            messages.success(request, f"You have unliked this post.")
        else:
            post.likes.add(request.user)
            messages.success(request, f"You have liked this post, thanks!")
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class BlogPost(generic.ListView):
    """Renders the blog page"""
    model = Post
    queryset = Post.objects.filter(status=1)
    template_name = 'blog.html'
    paginate_by = 6


def categories_view(request, cats):
    """Renders the posts filtered by categories"""
    categories_posts = Post.objects.filter(
        categories__title__contains=cats, status=1)
    return render(request, 'categories_posts.html', {
        'cats': cats.title(), 'categories_posts': categories_posts})


@login_required
def profile_view(request):
    """Renders the profile page"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)


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


@login_required
def delete_comment(request, comment_id):
    """Delete comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'The comment was deleted successfully')
    return HttpResponseRedirect(reverse(
        'post_detail', args=[comment.post.slug]))


class EditComment(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edite comment"""
    model = Comment
    template_name = 'edit_comment.html'
    form_class = CommentForm
    success_message = 'The comment was successfully updated'
