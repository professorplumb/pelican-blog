Authorization With mod_wsgi and the Importance Of Reading The FManual
#####################################################################

:slug: authorization-with-mod-wsgi
:tags: mod_wsgi, apache, www-authorization, django-tastypie
:status: draft

Quick one today.  I am a heavy user of the abbreviation :abbr:`RTFM (Read The Manual)` :html_entity:`mdash` mostly
because I'm an asshole. [1]_ But those who live by the sword die by the sword, and today I was a victim.  If you're into
schadenfreude, read on.

Authentication Consternation
============================

Background: I was deploying a `django-tastypie <https://github.com/toastdriven/django-tastypie>`_ API plus associated
client.  The client used HTTP authentication (via Tastypie's `BasicAuthentication
<https://github.com/professorplumb/django-tastypie/blob/master/tastypie/authentication.py#L76-147>`_ class) to
authenticate with the API, and everything worked fine on my local machine.

Once deployed, however, I can't log in.  I verify the credentials on the backend via the Django shell, and they work
fine.  I access the API directly, trying to log in via the browser's WWW-Authentication popup, and each time I log in
using what I am positive are the correct credentials, the damned popup pops back the hell up.

In retrospect, I spent far too long trying to figure out what was going on :html_entity:`mdash` I'll go into one of my
more desperate methods below.  Eventually, I sat back and asked myself: what was different between my local machine and
the deployed server?  Besides the operating system, the only difference was the method of serving pages: on my machine,
Django_ (for the API) and Flask_ (for the client) were serving them themselves; on the server, both were being served by
Apache_ using mod_wsgi_.  A-*ha*.

Shoulda Read the FM Part 1
==========================

I had other sites on the same server using Basic authentication, set up inside Apache's ``VirtualHost`` directive, as a
simple screen for unwanted visitors, and those worked fine.  So something was happening in between the browser and Django
to pervert or nullify my authentication attempts.  Flask wasn't the culprit, since the problem occurred when
authenticating directly with the API.  So one of Apache, mod_wsgi, Django, or Tastypie was the culprit.  To the
bat-code, Robin!

In ``tastypie.authentication``, inside ``BasicAuthentication``, the ``is_authenticated`` method tests the request's
``Authorization`` header to decode the username and password provided by the user.  Here's the first method I came up
with to see what the browser was sending: [2]_

.. code-block:: python

    def is_authenticated(self, request, **kwargs):
        """
        Checks a user's basic auth credentials against the current
        Django auth backend.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """
        if not request.META.get('HTTP_AUTHORIZATION'):
            // I added these two lines:
            import sys
            print >> sys.stderr, "Authenticated with ", request.META.get('HTTP_AUTHORIZATION')
            // tastypie code continues here
            return self._unauthorized()
        ...

The idea behind ``print >> sys.stderr`` is that the message will be printed to one of the error logs (Apache's server-wide
log or Django's site-specific one).  However, this wasn't working, and this is a problem I've run into before and haven't
yet solved.  Perhaps it will be a subject for a future post.

This is the first point when I should have :abbr:`RTFM (What do *you* think the 'F' stands for?)`.  The copious and
thorough ``mod_wsgi`` documentation suggests several `debugging techniques
<https://code.google.com/p/modwsgi/wiki/DebuggingTechniques>`_ which would have made my job a lot easier. [3]_  Instead,
this is what I came up with:

.. code-block:: python

    def is_authenticated(self, request, **kwargs):
        """
        Checks a user's basic auth credentials against the current
        Django auth backend.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """
        if not request.META.get('HTTP_AUTHORIZATION'):
            // I added this line:
            raise ValueError("Authenticated with " + str(request.META.get('HTTP_AUTHORIZATION')))
            // <sarcasm>brilliant.</sarcasm>
            return self._unauthorized()
        ...

Surprisingly, this worked :html_entity:`mdash` at least in the sense that I was making progress.  Here's what I got when
accessing the API via the browser:

.. code-block:: json

    {
    "error_message": "Authenticated with None",
    "traceback": "Traceback (most recent call last):\n\n [snip]"
    }

Huh.  So it looks like ``request.META.get('HTTP_AUTHORIZATION')`` is ``None``, which in hindsight makes sense because
it keeps returning Unauthorized, prompting the authentication popup.  I changed the value of the error to ``request.META``
and confirmed that ``HTTP_AUTHORIZATION`` was nowhere in that dict.

However, this is to be expected on the first request from the browser - that's what is happening inside the ``if``
block.  When the browser sends the first (unauthenticated) request, the server responds with a 401 Unauthorized per the
`HTTP Authentication spec <http://tools.ietf.org/html/rfc2617>`_.  What we're interested in is the response we get once
we send the authentication tokens.  For this, we use curl_:

.. code-block:: bash

    $  curl --user admin:[redacted] http://api-url.myhost.com/api/v1/resource/
    {"error_message": "Authenticated with None", "traceback": "Traceback (most recent call last):\n\n [snip] }

More progress: now it is apparent that even though curl is sending the authentication information, Tastypie is not
receiving it.  We have now confirmed that somewhere between Apache and mod_wsgi, the authorization header is being
stripped.  Since it works with Django and Tastypie on my local machine, and Apache serves other Basic-authenticated sites
on this same server, I now turn to mod_wsgi.

Pretty Fly For A WSGI
=====================

How often do you fully read the manual for software **before** you use it?  I tend to use the manuals as a reference
:html_entity:`mdash` skipping to the section I think I need, and then scrolling past paragraphs of exposition to look
for code blocks.  This is what I did with the mod_wsgi `access control mechanisms
<https://code.google.com/p/modwsgi/wiki/AccessControlMechanisms>`_ page, and the second place I should have
:abbr:`RTFM (I'm gonna say "FManual")`.

Scrolling down to the code blocks, I found a lot about how to `set up a WSGI authentication script
<https://code.google.com/p/modwsgi/wiki/AccessControlMechanisms#Apache_Authentication_Provider>`_.  "This isn't what I'm
looking for!", I mentally screamed as I paged through comprehensive but useless documentation.  "Why can't mod_wsgi just
pass the authentication through from Apache!?"

It took me an embarrassingly long amount of time searching StackOverflow and other sites before I was directed back to
the same page of the mod_wsgi documentation.  This time, reading the `very first subsection
<https://code.google.com/p/modwsgi/wiki/AccessControlMechanisms#HTTP_User_Authentication>`_, I found exactly what I was
looking for.  Adding this to my Apache VirtualHost configuration:

.. code-block:: text

     DocumentRoot /path/to/public_html/
     WSGIScriptAlias / /path/to/wsgi.py

     # this is the line which was added
     WSGIPassAuthorization On

produced this: [4]_

.. code-block:: bash

    $  curl --user admin:[redacted] http://api-url.myhost.com/api/v1/resource/
    {"error_message": "Authenticated with Basic YWRtaW46TmljZS1Ucnk=", "traceback": "Traceback (most recent call last):\n\n [snip] }

Eureka.  And now, when I remove the ValueError from the Tastypie code and go back to the API and client, both
authenticate successfully as they should have in the first place.

Wrapping Up
===========

It is tempting, when learning a new technology or researching an old one, to skim through the documentation in search
of the exact information you need.  It's also tedious and often overkill to read the entire manual before going to work.
However, doing so can save you frustration and time down the road when you're looking for something specific.  You
will at least know what information is available and where it is to be found ... since you
:abbr:`RTFM (http://xkcd.com/293/)`.

Footnotes
---------

.. [1] In my defense, though, I also used to name video game characters this.

.. [2] I'm breaking a couple programming rules here: modifying a library file, and also using ``print`` as a
        debugging tool.  I actually do both of these fairly often, for the simple reason that they're a lot quicker
        than setting breakpoints and firing up the debugger.  (It wasn't feasible in this case anyway since this was on
        a headless VPS.)

.. [3] mod_wsgi may not be the be-all and end-all of `WSGI implementations
        <http://wiki.python.org/moin/WSGIImplementations>`_, but its creator Graham Dumpleton deserves a lot of kudos
        for the comprehensive documentation as well as spending large amounts of time answering questions on StackOverflow
        and the like.  If you use mod_wsgi I strongly recommend `donating
        <https://code.google.com/p/modwsgi/#Contributing>`_.

.. [4] In the interests of clarity and brevity, I am leaving out steps where I moved the ValueError generation around
        inside the ``is_authenticated`` method.  In this case it must precede the ``if`` block to be shown.

.. _Django: https://www.djangoproject.com/
.. _Flask: http://flask.pocoo.org/
.. _Apache: http://apache.org/
.. _mod_wsgi: https://code.google.com/p/modwsgi/
.. _curl: http://curl.haxx.se/docs/httpscripting.html