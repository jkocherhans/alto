from alto.tests.decorators import view_decorator

def basic_view(request):
    """This is a basic test view."""
    pass

@view_decorator
def decorated_view(request):
    """This is a decorated function view."""
    pass
