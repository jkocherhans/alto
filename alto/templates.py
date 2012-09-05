import os
from django.conf import settings
from django.template import loader, TemplateDoesNotExist
from django.template.loader_tags import ExtendsNode


def find_template_source(name):
    """
    Load the source code and origin of the first template that matches the
    given name.
    """
    for loader_path in settings.TEMPLATE_LOADERS:
        template_loader = loader.find_template_loader(loader_path)
        try:
            source, origin = template_loader.load_template_source(name)
        except TemplateDoesNotExist:
            continue
        break
    return source, origin

def find_parents(name, parents=None):
    """
    Recursively find all of this template's parents and return them as a list.
    """
    template = loader.get_template(name)
    source, origin = find_template_source(name)
    if parents is None:
        parents = []
    else:
        parents.append({'name': name, 'file': origin})
    for node in template:
        if isinstance(node, ExtendsNode):
            parent_name = node.parent_name.token.strip('"')
            return find_parents(parent_name, parents)
    return parents

def find_template(name):
    source, origin = find_template_source(name)
    parents = list(reversed(find_parents(name)))
    return {'name': name, 'file': origin, 'source': source, 'parents': parents}

def find_templates():
    # Find all possible template directories.
    loaders = []
    for loader_path in settings.TEMPLATE_LOADERS:
        loaders.append(loader.find_template_loader(loader_path))

    paths = []
    for template_loader in loaders:
        temp_name = '__TEMP__.HTML'
        for path in template_loader.get_template_sources(temp_name):
            paths.append(path.strip(temp_name))

    # Find all possible templates in those template directories.
    for root_path in paths:
        for dirpath, dirnames, filenames in os.walk(root_path, followlinks=True):
            relative_path = os.path.relpath(dirpath, root_path)
            for filename in filenames:
                name = os.path.normpath(os.path.join(relative_path, filename))
                path = os.path.join(dirpath, filename)
                yield {'name': name, 'path': path}

if __name__ == '__main__':
    import json
    templates = list(find_templates())
    print json.dumps(templates, sort_keys=True, indent=2)
