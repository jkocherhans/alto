from django import http
from testproj import decorators

def require_login(view):
    """
    Decorator for requiring a logged-in user.
    """
    def wrapper(request, *args, **kwargs):
        return view(request, *args, **kwargs)
    return wrapper

def home(request):
    """
    The homepage.
    """
    return http.HttpResponse('home')

def about(request, test=False):
    """
    The about page.
    """
    return http.HttpResponse('about')

@require_login
def protected(request):
    """
    A protected page.
    """
    return http.HttpResponse('protected')

@require_login
@decorators.cache
def protected_and_cached(request):
    """
    A protected and cached page.
    """
    return http.HttpResponse('protected and cached')

def blog_detail(blog_id):
    """
    The detail page for a blog.
    """
    return http.HttpResponse('blog: %s' % blog_id)

def post_detail(blog_id, post_id):
    """
    The detail page for a blog post.
    """
    return http.HttpResponse('blog: %s post: %s' % (blog_id, post_id))

@decorators.DecoratorClass()
def decorated_with_instance():
    return http.HttpResponse('decorated_with_instance')
