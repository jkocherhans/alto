import ast
import inspect
import json
import re
from django.conf import settings
from django.core import urlresolvers


def extract_view(view, decorators=None):
    """
    Extract a view object out of any wrapping decorators.
    """
    # http://stackoverflow.com/questions/9222129/python-inspect-getmembers-does-not-return-the-actual-function-when-used-with-dec
    if decorators is None:
        decorators = []
    if view.func_closure is not None:
        decorators.append(view)
        return extract_view(view.func_closure[0].cell_contents, decorators)
    return view, decorators

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

def inspect_args(func):
    argspec = inspect.getargspec(func)
    return {
        'format': inspect.formatargspec(argspec.args, argspec.varargs, argspec.keywords, argspec.defaults),
        'args': argspec.args,
        'keywords': argspec.keywords,
        'defaults': argspec.defaults,
        'varargs': argspec.varargs,
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

def inspect_pattern(pattern):
    capture_groups = parse_capture_groups(pattern.regex.pattern)
    return {
        'regex': pattern.regex.pattern,
        'name': pattern.name,
        'default_args': pattern.default_args,
        'capture_groups': parse_capture_groups(pattern.regex.pattern)
    }

def main():
    patterns = []
    # This can't map out a url conf that is set on the request by middleware.
    urlconf = settings.ROOT_URLCONF
    urlresolvers.set_urlconf(urlconf)
    resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)
    for pattern in resolver.url_patterns:
        view, decorators = extract_view(pattern.callback)
        argspec = inspect.getargspec(view)
        pattern_data = inspect_pattern(pattern)
        source_lines, line_number = inspect.getsourcelines(view)
        view_data = {
            'file': inspect.getsourcefile(view),
            'name': view.__name__,
            'source': inspect.getsource(view),
            'sourcelines': source_lines,
            'line_number': line_number,
            'doc': inspect.getdoc(view),
            'decorators': [inspect_decorator(d) for d in get_decorators(view)],
            'args': inspect_args(view),
        }
        patterns.append({'pattern': pattern_data, 'view': view_data})
    print json.dumps(patterns, sort_keys=True, indent=2)

if __name__ == '__main__':
    main()
