Understanding Django's cached_property Decorator
################################################

:tags: django, functional, metaprogramming, genius
:category: code
:author: Eric Plumb
:summary: Writing a "cached property" decorator and exploring Django's implementation

There is not a lot of documentation out there about Django's ``cached_property`` decorator, which is one worth using.
Today I want to talk about what it does, how I discovered it, and explore how it works.

Let's get started with what it does and why you would use it.  How often, in Python or Django, do you find yourself
doing something like this:

.. code-block:: python

    class House():
        @property
        def color(self):
            if not getattr(self, '_color', None):
                self._color = load_color_from_db(self.id)
            return self._color

When objects have a method or property which is expensive to access (DB query, intensive calculation, etc.), it makes
sense to only make the effort to retrieve the value once.  This pattern allows you to access it subsequent times without
paying the cost for any access past the first.

However, it's somewhat clunky, and adds a namespace-polluting attribute to your object, and :html_entity:`mdash`
most of all :html_entity:`mdash` if you have
several properties with the same issue, you will find yourself repeating yourself a lot. [1]_

DIY DRY
=======

When I realized that this was a pattern worth abstracting, I wrote a ``cached_property`` decorator which looked
something like this:

.. code-block:: python

    def cached_property(method):
         prop_name = '_{}'.format(method.__name__)
         def wrapped_func(self, *args, **kwargs):
             if not hasattr(self, prop_name):
                 setattr(self, prop_name, method(self, *args, **kwargs))
             return getattr(self, prop_name)
         return property(wrapped_func)

Demonstrating its use: [2]_

.. code-block:: pycon

    >>> class House():
    ...     @property
    ...     def color(self):
    ...         print "Accessing color"
    ...         return "blue"
    ...     @cached_property
    ...     def square_footage(self):
    ...         print "Accessing square footage"
    ...         return 1500
    ...
    >>> h.color
    Accessing color
    'blue'
    >>> h.color  # Prints "Accessing color" each time you access the property
    Accessing color
    'blue'
    >>> h.square_footage
    Accessing square footage
    1500
    >>> h.square_footage  # Only prints message the first time
    1500

Serendipity
===========

I was pretty proud of myself after having written this decorator.  While I didn't like that it created extra attributes
on my object, it replaced lots of clunky ``if`` blocks with a clean decorator.

I immediately resolved to go through some Django projects and add the decorator to all the objects I'd previously been
using the first pattern on.  At some point, I typed ``@cached_property`` and activated autoimport, [3]_ and what to my
wondering eyes should appear but ``django.utils.functional.cached_property``!

What is this!?  Had my genius idea been pre-empted?  I imported it into my project and tried it out and: in a word, yes.
Its effect was precisely the same as that of my little handmade decorator.  (You can test this for yourself by trying
the console session above, replacing the decorator definition with ``from django.utils.functional import
cached_property``.)

Well, let's see if my version is any faster:

.. code-block:: pycon

    >>> timeit.timeit("""
    ... class House():
    ...     @cached_property
    ...     def color(self):
    ...         return 5
    ... """, setup="from django.utils.functional import cached_property")
    2.063973829377808
    >>> timeit.timeit("""
    ... class House():
    ...     @cached_property
    ...     def color(self):
    ...         return 5
    ... """, setup="""
    ... def cached_property(method):
    ...     prop_name = '_{}'.format(method.__name__)
    ...     def wrapped_func(self, *args, **kwargs):
    ...         if not hasattr(self, prop_name):
    ...             setattr(self, prop_name, method(self, *args, **kwargs))
    ...         return getattr(self, prop_name)
    ...     return property(wrapped_func)
    ... """)
    3.4206963438101354

I'm 75% slower; damn.  Well, I've been thoroughly outprogrammed here :html_entity:`mdash` all that's left is to look at
the Django code and see how they implemented this.

Django Knows
============

The code for this decorator is at https://github.com/django/django/blob/2456ffa42c33d63b54579eae0f5b9cf2a8cd3714/django/utils/functional.py#L38-50
and is reproduced below. [4]_

.. code-block:: python

    class cached_property(object):
        """
        Decorator that converts a method with a single self argument into a
        property cached on the instance.
        """
        def __init__(self, func):
            self.func = func

        def __get__(self, instance, type=None):
            if instance is None:
                return self
            res = instance.__dict__[self.func.__name__] = self.func(instance)
            return res

Remarkably simple for what it does.  It is a `class-based decorator
<http://stackoverflow.com/questions/6676015/class-decorators-vs-function-decorators>`_ rather than a more familiar
function-based one.  In addition to allowing it to keep state, this allows it to do something extremely clever and
audacious at the expense of extensibility.  Let's go through it briefly, using the following code as a concrete example.

.. code-block:: python

    class House(object):
        @cached_property
        def color(self):
            return "blue"

1. ``__init__``
    The ``__init__`` method of a class-based decorator is called when its decorated function is defined (in this case
    at class definition time), with its only argument besides the omnipresent ``self`` being the decorated function.
    The ``cached_property`` decorator class simply stores this function (a method, in this case) for future reference.
    Important for the next item is that at this point, ``House.color`` is a ``cached_property`` object instance.

2. ``__get__``
    Those of you who use class-based decorators are probably more familiar with implementing the decoration logic in the
    ``__call__`` method.  This is where the genius comes in: if ``h`` is a ``House`` instance, at the time the
    ``h.color`` attribute
    is accessed, if it points to an object like the current ``cached_property`` instance, Python calls the special
    ``__get__()`` descriptor method of that object.  (This object's class is in fact referred to as a *descriptor class*
    in `the docs <http://docs.python.org/2/reference/datamodel.html#implementing-descriptors>`_, and the containing
    class (``House`` in this case) as the *owner class*.)

    The arguments to ``__get__()`` are as follows:

    * ``self``, the current ``cached_property`` instance, on which the original method is stored as ``self.func``

    * ``instance``, the instance of the *owner class* :html_entity:`mdash` in this case ``h``.  This is essentially a second ``self`` argument, with the instance in this case being the one we actually care about.

    * ``type``, the class type of the *owner class* :html_entity:`mdash` in this case ``House``.

    With this in mind, look at what ``__get__()`` does.  Ignore the ``if`` block for now and let's focus on the next
    line, starting from the right and going left.

    1. ``self.func(instance)``
        calls the original (decorated) method which was cached as ``self.func`` under this ``cached_property`` instance
        at definition time.  The ``instance`` argument it passes is the ``House`` instance which ``color`` was
        referenced from.  Normally, when you call an instance method, this first argument would be named ``self``.

        See where this is going?  ``self.func(instance)`` is the same as calling ``h.color()`` (or ``House.color(h)``)
        if you hadn't decorated the method at all.

    2. ``instance.__dict__[self.func.__name__]``
        is where the magic happens.  It asks ``self.func`` what its ``__name__``
        is (in this case ``color``), then uses the instance's ``__dict__`` attribute to *replace itself with a property
        consisting of the value calculated in step 1.*  In other words, before this statement is executed, ``h.color``
        refers to a ``cached_property`` instance.  After it is executed, ``h.color`` refers to the string "blue".  What
        this instance is doing, *at the very time it's being accessed*, is replacing itself with the value calculated
        by the decorated method.

    3. ``res = ...``
        It's all over now but for the cleanup.  The calculated value is passed to a temporary variable which is then
        ``return`` ed so that this invocation of ``cached_property.__get__()`` (accessed via ``h.color``) returns the
        value ("blue") which is now stored as the property ``h.color``.

    So that's ``cached_property.__get__()``, which selflessly overwrites its containing instance with a dumb value.
    Once out of the scope of this function, the ``cached_property`` instance is no longer referred to and can be
    garbage-collected.

3. ``if instance is None: return self``
    Briefly on this: this is relevant when the ``color`` attribute is accessed via the class instead of an instance, e.g.
    ``House.color`` instead of ``h.color``.  It simply returns the ``cached_property`` instance itself.  This isn't all
    that useful to the user, and I assume it's just done to avoid a ``TypeError`` when the cached function would otherwise
    be called with a ``None`` instance. [5]_

So that's what some brilliant mind on the Django team came up with.  Being able to "monkeypatch" attributes and properties
is one of the benefits of any dynamic language, but seldom have I seen it used so audaciously.  It also shows the power
of Python's double-underscore descriptors, which continue to amaze me in what they are capable of.

Now that I'm done gushing, one note about this decorator is that it will only work for object methods, not pure functions.
Can you tell why?  This is one downside of this method over the function-based decorator :html_entity:`mdash` that one
could fairly easily be extended to work on any function.  However, it would be just as easy to write a module-level
version of this decorator.

Wrapping Up
===========

The links above on class-based decorators and Python's descriptor methods are both worth reading in their entirety.  Both
helped me understand what was going on in Django's ``cached_property`` definition, especially understanding the double
level of indirection (i.e., inside ``cached_property.__get__()``, ``self`` represents the ``cached_property`` object
whereas ``instance`` represents the object whose method it's decorating) and the use of ``__get__`` instead of the
more familiar ``__call__``.

If you read this far, thanks!  Comments and corrections are always appreciated.

Footnotes
---------

.. [1] I initially typed "if you have several properties with this same property."  Talk about repeating yourself
       repeating yourself.

.. [2] Note that if you try this example in an IDE or console with autocomplete, you may find it printing the "Accessing"
       messages as soon as you have typed ``h.``.  This is because your console is accessing the properties as it tries
       to inspect which properties/methods are on the object in order to bring up the autocomplete options.  You can
       test this by copy/pasting "h.color" which gives it no time to autocomplete.

.. [3] ``Ctrl + Shift + O`` in Eclipse, ``Alt + Enter`` while on the unimported name in IDEA.  Of course you knew
       this already, but for those who didn't: you're welcome.

.. [4] Updated 7/25/13 to reflect changes in Django codebase :html_entity:`mdash` Django 1.4.0, about which I originally
        wrote this article, did not have the ``if instance is None`` check.

.. [5] A side effect of this is that if you implemented a ``__call__`` method on ``cached_property`` which simply
        returned ``self.func(instance)``, you could then use ``House.color(h)`` as a way to get the value via a
        function call instead of attribute access.  This isn't much more than a parlor trick though.