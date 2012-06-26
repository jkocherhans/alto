# import functools
# functools.wraps gets the docsting and name right, but the function
# signature, file, etc wrong.

def cache(view):
    """
    Decorator for requiring a caching a view.
    """
    def wrapper(request, *args, **kwargs):
        return view(request, *args, **kwargs)
    return wrapper
