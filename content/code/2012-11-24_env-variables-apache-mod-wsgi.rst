Passing Apache Environment Variables to Django via mod_wsgi
###########################################################

:tags: apache, django, mod_wsgi, flask

When you have an application that will be deployed on multiple sites or in multiple environments (e.g. local development,
staging, QA, production), one of the easiest ways to deal with environment-specific variables like database
name/user/password or secret key is to let them be set by the server environment.

To use Django_ as an example, in your ``settings.py`` you'd do something like:

.. code-block:: python

    import os
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            ...
        }
    }

When developing, you can then set ``DB_NAME`` and ``DB_USER`` environment variables in your project IDE and/or
interpreter.

However, when you deploy remotely and Django is running under a web server like Apache_ or nginx_ using mod_wsgi_, you
have to have the web server pass the environment variables. [1]_  In an Apache VirtualHost configuration it would look
like this:

.. code-block:: text

    <VirtualHost *:80>
         ServerAdmin webmaster@example.com
         ServerName example.com
         ServerAlias example.com

         SetEnv DB_NAME mydatabase
         SetEnv DB_USER mydbuser
         SetEnv DB_PASSWD sekrit
         SetEnv DB_HOST localhost

         DocumentRoot /path/to/public_html/
         WSGIScriptAlias / /path/to/app/app_name/wsgi.py

         Alias /static /path/to/public_html/static
         Alias /media /path/to/public_html/media

         ErrorLog /path/to/logs/error.log
         CustomLog /path/to/logs/access.log combined
    </VirtualHost>

We're almost there.  When you reload Apache and run your application, you will get a ``KeyError`` when your
``settings.py`` tries to access the environment variables.  This is because mod_wsgi does not pass OS environment
variables to the underlying application by default.  You will need to have it set them manually.  Here is a sample
``wsgi.py`` file for Django:

.. code-block:: python

    import os, site, sys

    site.addsitedir('/usr/local/virtualenvs/MYAPP-VIRTUALENV/lib/python2.7/site-packages')

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(BASE_DIR, '..'))

    os.environ["DJANGO_SETTINGS_MODULE"] = "myapp.settings"  # see footnote [2]

    from django.core.wsgi import get_wsgi_application
    _application = get_wsgi_application()

    env_variables_to_pass = ['DB_NAME', 'DB_USER', 'DB_PASSWD', 'DB_HOST', ]
    def application(environ, start_response):
        # pass the WSGI environment variables on through to os.environ
        for var in env_variables_to_pass:
            os.environ[var] = environ.get(var, '')
        return _application(environ, start_response)

The variables we declare in Apache are passed to the WSGI application via its ``environ`` parameter.  We simply
explicitly set these in ``os.environ`` so that the underlying Django application can access them. (Also see footnote
[2]_ regarding the annotated line in the above code.)

If you don't want to explicitly declare the variables to pass, you can preface each with ``MYAPP_`` in the VirtualHost
configuration, then do:

.. code-block:: python

    for key in environ:
        if key.startswith('MYAPP_'):
            os.environ[key] = environ[key]

For Flask_ users, the same ``wsgi.py`` would look something like:

.. code-block:: python

    import os, site, sys

    site.addsitedir('/usr/local/virtualenvs/MY-VIRTUALENV/lib/python2.7/site-packages')

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(BASE_DIR, '..'))


    def application(environ, start_response):
        for key in ['DB_NAME', 'DB_USER', 'DB_PASSWD', 'DB_HOST', 'SECRET_KEY', ]:
            os.environ[key] = environ.get(key, '')
        from mmf_lexicon_client.application import app as _application

        return _application(environ, start_response)

Note that the Flask ``app`` is imported inside the ``def application`` block :html_entity:`mdash` if you import it
outside of this block, you won't be able to use the environment variables at the Flask ``app`` level or any file which
is imported on application load.  This is because the WSGI application hasn't loaded at the time you import the Flask
application, so it can't pass the environment variables yet.

Wrapping Up
===========

Hope this helps!  This is a very common use pattern for me, and one for which I didn't find very useful documentation
when I first started looking for a solution.  As always, comments and questions are welcome.

Footnotes
---------

.. [1] If your app is the only one running on this server which will need these environment variables, you can of course
        set them system- or interpreter-wide.  In this case we're assuming that we need to set them on a per-VirtualHost
        basis.

.. [2] Django's ``wsgi.py`` template has this line as ``os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")``.
        To see why this can bite you, see `this StackOverflow answer <http://stackoverflow.com/a/11515629/1094910>`_ by
        mod_wsgi's creator Graham Dumpleton.

.. _Django: https://www.djangoproject.com/
.. _Flask: http://flask.pocoo.org/
.. _Apache: http://apache.org/
.. _mod_wsgi: https://code.google.com/p/modwsgi/
.. _nginx: http://wiki.nginx.org/Main