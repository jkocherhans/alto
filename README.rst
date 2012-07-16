====
Alto
====

This Django app allows you to browse the urlpatterns for your project, see the source code of each view, and open that code in your favorite editor [*]_.

Planned features include the ability to browse and search for apps, models, templates, tags, filters, and celery tasks.

Possibly planned features are for Alto to become a `Light Table`_ plugin.

Alto is PRE-ALPHA software. It probably won't work with your project. There is no support. Unless you're ready to work on it, you should hold off for a few releases.

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
2. Add ``url(r'^_alto/', include('alto.urls'))`` to your urlaptterns
3. Visit http://127.0.0.1:8000/_alto/
4. Add ``ALTO_URL_SCHEME = 'txmt'`` to your settings for TextMate support. The default is ``'mvim'``.

This will expose the source code of your site, so be sure to take proper precautions like only enabling the url pattern if ``DEBUG=True``.


Thanks
------

Alto is inspired by `Bret Victor`_'s talk, "`Inventing on Principle`_" and by `Light Table`_.

.. _`Bret Victor`: http://worrydream.com/
.. _`Inventing on Principle`: http://vimeo.com/36579366


.. [*] As long as your favorite editor is MacVim or TextMate. In theory, any editor that can be made to open a file from a custom url scheme will work.
