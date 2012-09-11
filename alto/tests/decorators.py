def decorator_function(view):
    """A  basic view decorator."""
    def wrapper(request):
        return view(request)
    return wrapper

class DecoratorClass(object):
    def __call__(self, view):
        def wrapper(request, *args, **kwargs):
            return view(request, *args, **kwargs)
        return wrapper
