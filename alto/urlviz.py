import ast
import inspect
import json
import re
from django.conf import settings
from django.core import urlresolvers
from django.utils import regex_helper


# URLs ########################################################################

def get_resolver_data(resolver, prefix=None):
    patterns = []
    resolver_prefix = getattr(getattr(resolver, 'regex'), 'pattern')
    prefix = prefix + resolver_prefix if prefix else resolver_prefix
    for pattern in resolver.url_patterns:
        if isinstance(pattern, urlresolvers.RegexURLResolver):
            patterns.extend(get_resolver_data(pattern, prefix=prefix))
        elif isinstance(pattern, urlresolvers.RegexURLPattern):
            view, decorators = extract_view(pattern.callback)
            pattern_data = inspect_pattern(pattern, prefix=prefix)
            patterns.append(pattern_data)
        else:
            raise Exception('Unknown object: %s', pattern)
    return patterns

def inspect_urlpatterns():
    # This can't map out a url conf that is set on the request by middleware.
    urlconf = settings.ROOT_URLCONF
    urlresolvers.set_urlconf(urlconf)
    resolver = urlresolvers.RegexURLResolver(r'', urlconf)
    return get_resolver_data(resolver)

def inspect_pattern(pattern, prefix=None):
    prefix = prefix or ''
    view, decorators = extract_view(pattern.callback)
    module = inspect.getmodule(view)

    if inspect.isfunction(view):
        argspec = inspect.getargspec(view)
    else:
        argspec = None

    annotations = {}
    group_names = {}
    normalized_pattern, groups = regex_helper.normalize(prefix + pattern.regex.pattern)[0]
    for group in groups:
        try:
            group_number = int(group.strip('_'))
        except ValueError:
            group_number = None
        if argspec is not None and group_number is not None:
            try:
                group_name = argspec[0][group_number + 1]
            except IndexError:
                group_name = group
        else:
            group_name = group
        annotations[group] = '<span class="capturegroup">&lt;%s&gt;</span>' % group_name
        group_names[group] = group_name

    return {
        'view_module': module.__name__,
        'view_name': view.__name__,
        'prefix': prefix,
        'regex': pattern.regex.pattern,
        'name': pattern.name,
        'default_args': str(pattern.default_args),
        'annotated_pattern': normalized_pattern % annotations,
        'normalized_pattern': normalized_pattern % group_names,
        'raw_pattern': prefix + pattern.regex.pattern,
    }

def parse_capture_groups(regex):
    capture_groups = []
    capture_group_re = re.compile(r'(\([^\)]+\))')
    name_re = re.compile(r'\?P<([^>]+)>')
    for pattern in capture_group_re.findall(regex):
        m = name_re.search(pattern)
        if m is None:
            name = None
        else:
            name = m.group(1)
        capture_groups.append({'name': name, 'pattern': pattern})
    return capture_groups


# Views #######################################################################

def load_view(module_path, view_name):
    import importlib
    module = importlib.import_module(module_path)
    return getattr(module, view_name)

def inspect_view(view):
    source_lines, line_number = inspect.getsourcelines(view)
    data = {
        'file': inspect.getsourcefile(view),
        'name': view.__name__,
        'source': inspect.getsource(view),
        'sourcelines': source_lines,
        'line_number': line_number,
        'doc': inspect.getdoc(view),
        #'decorators': [inspect_decorator(d) for d in get_decorators(view)],
        #'args': inspect_args(view),
    }
    return data

def extract_view(view, decorators=None):
    """
    Extract a view object out of any wrapping decorators.
    """
    # http://stackoverflow.com/questions/9222129/python-inspect-getmembers-does-not-return-the-actual-function-when-used-with-dec
    if decorators is None:
        decorators = []
    if getattr(view, 'func_closure', None) is not None:
        decorators.append(view)
        for closure in view.func_closure:
            if callable(closure.cell_contents):
                return extract_view(closure.cell_contents, decorators)
    if inspect.isfunction(view) or inspect.ismethod(view):
        pass
    elif inspect.isclass(view):
        pass
    else:
        view = view.__class__
    return view, decorators

def inspect_args(func):
    argspec = inspect.getargspec(func)
    return {
        'format': inspect.formatargspec(argspec.args, argspec.varargs, argspec.keywords, argspec.defaults),
        'args': argspec.args,
        'keywords': argspec.keywords,
        'defaults': argspec.defaults,
        'varargs': argspec.varargs,
    }


# Decorators ##################################################################

def get_decorators(func):
    """
    Return a list of decorator names for this function.
    """
    decorators = []
    # Parse the source code of the function with ast to find the names of
    # all of its decorators.
    tree = ast.parse(inspect.getsource(func))
    for node in ast.iter_child_nodes(tree):
        for dnode in node.decorator_list:
            if isinstance(dnode, ast.Name):
                decorator = func.func_globals[dnode.id]
            elif isinstance(dnode, ast.Attribute):
                module = func.func_globals[dnode.value.id]
                decorator = getattr(module, dnode.attr)
            else:
                raise Exception("Unable to handle decorator node: %s" % dnode)
            decorators.append(decorator)
    return decorators

def inspect_decorator(decorator):
    return {
        'file': inspect.getsourcefile(decorator),
        'name': decorator.__name__,
        'doc': inspect.getdoc(decorator),
        'source': inspect.getsource(decorator),
        'args': inspect_args(decorator),
    }


if __name__ == '__main__':
    patterns = inspect_urlpatterns()
    print json.dumps(patterns, sort_keys=True, indent=2)
