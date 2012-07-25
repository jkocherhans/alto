from alto.tests.decorators import view_decorator

def basic_view(request):
    """This is a basic test view."""
    pass

@view_decorator
def decorated_view(request):
    """This is a decorated function view."""
    pass

class ClassView(object):
    """This is a basic class view."""
    def __call__(request):
        pass

def single_positional_arg(request, id):
    pass

def single_keyword_arg(request, slug=None):
    pass
