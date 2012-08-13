import os
from django.conf import settings
from django.template.loader import find_template_loader

def find_templates():
    # Find all possible template directories.
    loaders = []
    for loader_path in settings.TEMPLATE_LOADERS:
        loaders.append(find_template_loader(loader_path))

    paths = []
    for loader in loaders:
        temp_name = '__TEMP__.HTML'
        for path in loader.get_template_sources(temp_name):
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
