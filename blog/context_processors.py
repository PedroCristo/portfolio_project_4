from posts.models import *


def extras(request):
    """Show categories list in the entire application"""
    categories = Category.objects.all()
    context = {
        'categories_list': categories
    }

    return context
