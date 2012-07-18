def view_decorator(view):
    """A  basic view decorator."""
    def wrapper(request):
        return view(request)
    return wrapper

