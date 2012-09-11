from alto.tests import decorators

def basic_view(request):
    """This is a basic test view."""
    pass

@decorators.decorator_function
def function_decorated_view(request):
    """This is a decorated function view."""
    pass

@decorators.DecoratorClass()
def instance_decorated_view(request):
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
