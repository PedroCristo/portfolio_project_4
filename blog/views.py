from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse, redirect, resolve_url
from django.views import generic, View
from django.contrib import messages
from posts.models import *
from .forms import CommentForm, UserUpdateForm, ProfileUpdateForm



def index(request):
    """View to return the index page"""
    queryset = Post.objects.filter(featured=True
    ).order_by('-timestamp')

    context = {
        'post_list': queryset,
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
            messages.success(request, f"Your comment was sent successfully and is awaiting approval!")
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
            messages.success(request, f"You have unliked this post.")
        else:
            post.likes.add(request.user)
            messages.success(request, f"You have liked this post, thanks!")
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))         


def about(request):
    """View to return the about page"""
    return render(request, 'about.html')   


class BlogPost(generic.ListView):
    """View to return the blog page"""
    model = Post
    template_name = 'blog.html'
    paginate_by = 6


def contact(request):
    """View to return the contact page"""

     #Get data from the contact form
    if request.method == 'POST':
        name = request.POST['name']
        name = name.capitalize()
        # surname = request.POST['surname']
        # subject = request.POST['subject']
        # email = request.POST['email']
        # message = request.POST['message']

        # #Send an email
        # send_mail(
        #     subject,
        #     message,
        #     email,
        #     ['pedro.web.test@gmail.com'],
        # )
        messages.success(request, f"Your email has been sent!")
        return render(request, 'contact.html', {'name': name})
    else:        
        return render(request, 'contact.html')



def categories(request):
    """View to return the categories page"""
    return render(request, 'categories.html')   


def CategoriesView(request, cats): 
    """View to return the posts filtered by categories""" 
    categories_posts = Post.objects.filter(categories__title__contains=cats)
    return render(request, 'categories_posts.html', {
        'cats':cats.title(), 'categories_posts':categories_posts })

def ProfileView(request): 
    """View to return the profile page""" 
    if request.method == 'POST':
      user_form = UserUpdateForm(request.POST,instance=request.user)
      profile_form = ProfileUpdateForm(request.POST,
                                 request.FILES,
                                 instance=request.user.profile)
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


def delete_comment(request, comment_id):
    """Delete comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Your comment was deleted successfully')
    return HttpResponseRedirect(reverse(
        'post_detail', args=[comment.post.slug]))        
