====
Alto
====

This Django app allows you to browse the urlpatterns, views, and templates for
your project, see their source code, and open that code in your favorite editor
[*]_.

Planned features include the ability to browse and search for models, template
tags, filters, and celery tasks.

At some point, Alto may become a `Light Table`_ plugin.

Alto is ALPHA software. It may or may not work with your project. Bug reports
without patches are unlikely to be fixed for now, so unless you're ready to work
on it, you should hold off for a few releases.

.. _`Light Table`: http://www.chris-granger.com/2012/04/12/light-table---a-new-ide-concept/

Requirements
------------

* Python 2.7
* Django 1.4

Other versions may work, but have not been tested.


Installation
------------

``pip install alto``


Setup
-----

1. Add ``'alto'`` to your ``INSTALLED_APPS``
2. Add ``'alto.middleware.AltoMiddleware'`` to your ``MIDDLEWARE_CLASSES``
3. Visit http://127.0.0.1:8000/_alto/

.. image:: https://s3.amazonaws.com/jkocherhans/alto/templates.png
   :width: 600
   :target: https://s3.amazonaws.com/jkocherhans/alto/templates.png

Configuration
-------------
Set ``ALTO_URL_SCHEME`` in your Django settings. The default is ``'mvim'`` for
opening files in MacVim. ``'txmt'`` will work for TextMate, and if you install
`SublHandler`_, ``'subl'`` will open Sublime Text 2.

.. _`SublHandler`: https://github.com/asuth/subl-handler

Thanks
------

Alto is inspired by `Bret Victor`_'s talk, "`Inventing on Principle`_" and by
`Light Table`_.

.. _`Bret Victor`: http://worrydream.com/
.. _`Inventing on Principle`: http://vimeo.com/36579366


.. [*] As long as your favorite editor is MacVim, TextMate or Sublime Text 2. In theory, any editor that can be made to open a file from a custom url scheme will work.
