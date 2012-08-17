import os
from django.conf import settings
from django.template import loader


def find_template(name):
    template = loader.get_template(name)
    template_path = template.origin.name
    with open(template_path, 'r') as fh:
        source = fh.read()
    return {'name': name, 'file': template_path, 'source': source}

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
