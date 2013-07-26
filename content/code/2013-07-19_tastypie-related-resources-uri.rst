The Rule of Three: Related Resources URIs with Tastypie
#######################################################

:tags: django, tastypie
:category: code
:author: Eric Plumb
:summary: Add a URI for a collection of related resources to a resource detail in Django-Tastypie

There are several `Rules <http://chriskrycho.com/web/good-programming-in-3-simple-rules>`_
`of <http://en.wikipedia.org/wiki/Rule_of_three_(C%2B%2B_programming)>`_
`Three <http://martinfowler.com/bliki/TwoHardThings.html>`_ in programming.
One of my favorites :html_entity:`mdash` and one I followed unwittingly for a while
before realizing it was codified :html_entity:`mdash` is the one about `when to refactor
<http://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)>`_ a single use case into a reusable pattern.
I encountered exactly this issue yesterday
while developing a `django-tastypie <https://github.com/toastdriven/django-tastypie>`_ API.  My experience extracting the
single- and then double-use case into a general-case pattern is documented here.

An issue that comes up a lot when developing resources in Tastypie is what to do when one of your resources contains
or should reference a list of related resources.  For example, let's say I'm writing an API for a dessert recipe
service. [1]_
I might have a ``DessertCategoryResource`` (e.g. pies, cakes, etc.) which points to a collection of ``RecipeResources``
which would look something like this: [2]_

.. code-block:: python

    from tastypie import resources, fields

    class DessertCategoryResource(resources.ModelResource):
        name = fields.CharField(attribute='name')
        ...

    class DessertRecipeResource(resources.ModelResource):
        category = fields.ForeignKey(DessertCategoryResource, 'category_parent')
        name = fields.CharField(attribute='name')
        recipe_text = fields.TextField(attribute='recipe_text')
        ...

Now when displaying a ``DessertCategoryResource`` I have a couple options for displaying its related recipes.  One is
to display them inline as nested resources:

.. code-block:: python

    class DessertCategoryResource(resources.ModelResource):
        name = fields.CharField(attribute='name')
        recipes = fields.ToManyField(DessertRecipeResource, 'dessertrecipe_set')
        ...

which would display something like this in the list view of ``DessertCategoryResource``:

.. code-block:: json

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects":  [
            {
                "name": "Pies",
                "resource_uri": "/api/v1/category/1/",
                "recipes": [
                    "/api/v1/recipes/1/",
                    "/api/v1/recipes/2/"
                ]
            },
            {
                "name": "Cakes",
                "resource_uri": "/api/v1/category/2/",
                "recipes": [
                    "/api/v1/recipes/3/",
                    "/api/v1/recipes/4/"
                ]
            }
        ]
    }

This format obviously requires a separate API call to get each recipe in a category, which is less than ideal.  If I
wanted to display the full recipe records in the "recipes" field instead of just the URIs, I would just pass
``full=True`` to the ``fields.ToManyField`` constructor in ``DessertCategoryResource``.  However, this could be a lot
of data to return to the client.  Is there a way to get the best of both worlds?

Related Yet Separate
====================

What I would like to do in this situation is have a "related resources" URI for each category, which the API consumer
can follow to get the recipes for each category, but only if she wants to.  For the Pies category above, which is at
``/api/v1/category/1/``, I want this URI to be ``/api/v1/category/1/recipes/``.  Here is what that could look like in
Tastypie:

.. code-block:: python

    class DessertCategoryResource(resources.ModelResource):
        ...

        def get_recipes(self, request, **kwargs):
            self.method_check(request, ['get', ])
            return DessertRecipeResource().get_list(request, category=kwargs['pk'])

        def prepend_urls(self):
            return [
                url(r'^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/recipes%s$' % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('get_recipes'),
                    name='api_get_recipes_for_category')
            ]

        def dehydrate(self, bundle):
            kwargs = dict(api_name='v1', resource_name=self._meta.resource_name, pk=bundle.data['id'])
            bundle.data['recipes_uri'] = reverse('api_get_recipes_for_category', kwargs=kwargs)

            return bundle

    class DessertRecipeResource(resources.ModelResource):
        ...

        class Meta:
            ...
            filtering = {'category': ["exact", ]}

Let's walk through this from the top down.

1. get_recipes()
    This is the actual "view" which shows the related recipes.  It confirms that the client is performing a
    GET request (more on this below) and returns the related recipe resources (i.e., those which have
    this category's ``pk`` in their ``category`` field.)
2. prepend_urls()
    prepend_urls is Tastypie's way of allowing you to define additional URLs by which this resource can be accessed.
    Here we copy the ``dispatch_detail`` URL and append "/recipes" to it to give us the URL by which the related
    recipes can be accessed.
3. dehydrate()
    The recipes URL is no good if clients don't know it exists :html_entity:`mdash` we need it to appear on the serialized view of the
    category resource. The ``dehydrate`` function converts a back-end object instance to a serialized resource
    representation to return to the client.
    Tastypie does the conversion of the object (a ``DessertCategory`` model instance in this case) for us, and provides
    the ``dehydrate`` method so that we can provide additional information.  Here we add the ``recipes_uri`` field which
    references the ``api_get_dessert_category_recipes`` URL name we defined.
4. DessertRecipeResource.Meta.filtering
    Simply lets ``DessertRecipeResource`` know that it is allowed to filter on the ``category`` ForeignKey field.
    Without this, Tastypie would throw an error, as the default is to not allow filtering on any fields.

And that's it!  Now we can access ``/api/v1/category/1/recipes/`` in our client and see the full list of recipes:

.. code-block:: json

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects": [
            {
                "category": "/api/v1/category/1/",
                "name": "Blackberry Pie",
                "recipe_text": "..."
            },
            {
                "category": "/api/v1/category/1/",
                "name": "Lemon Meringue Pie",
                "recipe_text": "..."
            }
        ]
    }

Extending Relations
===================

However, this is not very extensible.  If I wanted to use this same pattern on another pair of base/related resources, I
would have to copy/paste this code into that resource, and then change class, view, and URL names.
This isn't very :abbr:`DRY (Don't Repeat Yourself)`.  Likewise, if I want to add a second related resource to
``DessertCategory``, I have to add a new view function, and a line or two each to ``dehydrate`` and ``prepend_urls``.

What I want is a monkeypatch which will dynamically add the view method to a given resource class and also create the
``dehydrate()`` and ``prepend_urls()`` methods.  This seems straightforward to do as a mixin, something like:

.. code-block:: python

    class RelatedResourceURIMixin(object):
        def __init__(self, related_resource_class, related_resource_name, related_resource_fk_field_name):
            self._related_resource_class = related_resource_class
            self._related_resource_name = related_resource_name
            self._related_resource_url_name = 'api_get_{}_for_{}'.format(self._related_resource_name,
                                                                         self._meta.resource_name)

        def _related_resource_view(self, request, **kwargs):
            self.method_check(request, ['get', ])
            return related_resource_class().get_list(request, **{related_resource_fk_field_name: kwargs['pk']})

        def dehydrate(self, bundle):
            kwargs = dict(api_name='v1', resource_name=self._meta.resource_name, pk=bundle.data['id'])
            bundle.data['{}_uri'.format(self._related_resource_name)] = \
                reverse(self._related_resource_url_name, kwargs=kwargs)

        def prepend_urls(self):
            return [
                url(r'^(?P<resource_name>{})/(?P<pk>\w[\w/-]*)/{}{}$'.format(self._meta.resource_name,
                                                                             self._related_resource_name,
                                                                             trailing_slash()),
                    self.wrap_view('_related_resource_view'),
                    name=self._related_resource_url_name)
            ]

This looks good at first glance :html_entity:`mdash` our base resource class can inherit from this as well as ``ModelResource``, and we
pass the class, name, and FK field name (for the ForeignKey to the base resource) to the constructor.  But wait :html_entity:`mdash` where
do we call the constructor?  Tastypie is creating these resources for us behind the scenes, and passing extra arguments
would require updating Tastypie code.  We could set the ``_related_resource_class`` and other attributes in the resource
class definition, but that defeats the purpose of having just a single patch.

Similarly, what if we want to add a *second* related resource?  We can't inherit from the same mixin twice, and even
if we could, the second one's methods would clobber the first's.  Likewise, if the resource we're extending
already has custom ``dehydrate`` or ``prepend_urls`` classes defined, those will override this mixin's methods.

Patching Without Overriding
---------------------------

So back to the drawing board.  What we need is a way to *extend* a method without overriding it :html_entity:`mdash` in other words, to
add a value to the bundle returned by the existing ``dehydrate`` method, or append a new URL to the list returned by
``prepend_urls``.  Since this issue has cropped up for me more than twice before, I have a ready-made decorator:

.. code-block:: python

    def patch_class_func(cls, func_name):
        def wrapped_new_func(new_func):
            orig_func = getattr(cls, func_name)
            def call_new_func_on_return_value_of_old(self, *args, **kwargs):
                return new_func(self, orig_func(self, *args, **kwargs))
            setattr(cls, func_name, call_new_func_on_return_value_of_old)
        return wrapped_new_func

If you aren't familiar with `decorators with arguments <http://www.artima.com/weblogs/viewpost.jsp?thread=240845>`_,
they can seem intimidatingly complex at first.  Delving into how this works is beyond the scope of this post; I suggest
reading the link above as well as `this StackOverflow answer
<http://stackoverflow.com/questions/5929107/python-decorators-with-parameters>`_ which is less in-depth and more
digestible.

Here is a (silly) example of how to use the decorator.  We are going to patch ``collections.OrderedDict`` to
surreptitiously add an additional entry each time its ``copy()`` method is called.  (Extra credit if you can tell me
why I am demonstrating this on ``OrderedDict`` instead of just ``dict``.)

.. code-block:: pycon

    >>> from collections import OrderedDict
    >>>
    >>> @patch_class_func(OrderedDict, 'copy')
    ... def kilroy_was_here(self, orig_copied_dict):
    ...     orig_copied_dict['kilroy'] = "was here"
    ...     return orig_copied_dict
    ...
    >>> od = OrderedDict(a=1, b=2, c=3)
    >>> od.copy()
    OrderedDict([('a', 1), ('b', 2), ('c', 3), ('kilroy', 'was here')])

Mixing It In
------------

We now have all the pieces in place to be able to create a reusable function which will create or patch the relevant
resource methods without clobbering them.  Without further ado:

.. code-block:: python

    def add_related_uri_to_resource(resource_class, related_resource_name, related_resource_class, related_resource_fk_field_name):
        base_resource_name = resource_class.Meta.resource_name

        uri_key = '{}_uri'.format(related_resource_name)
        url_name = 'api_get_{}_for_{}'.format(related_resource_name, base_resource_name)
        view_func_name = 'get_{}'.format(related_resource_name)

        @patch_class_func(resource_class, 'dehydrate')
        def wrap_dehydrate(self, dehydrated_bundle):
            # build related resource URI
            kwargs = dict(api_name='v1', resource_name=base_resource_name, \
                          pk=dehydrated_bundle.data[self._meta.object_class._meta.pk.name])
            dehydrated_bundle.data[uri_key] = reverse(url_name, kwargs=kwargs)
            return dehydrated_bundle

        @patch_class_func(resource_class, 'prepend_urls')
        def wrap_prepend_urls(self, url_list):
            # copy the detail URL for the base resource
            dispatch_detail_url = [u for u in self.base_urls() if u.name == 'api_dispatch_detail'][0]

            # append the related resource name to it
            related_url_pattern = dispatch_detail_url.regex.pattern.rstrip('$?/')
            related_url_pattern = r'{}/{}{}$'.format(related_url_pattern, related_resource_name, trailing_slash())

            # and create the URL pattern for the related resource list view
            url_list.append(url(related_url_pattern, self.wrap_view(view_func_name), name=url_name))
            return url_list

        def get_related_list(self, request, **kwargs):
            # allow only GET requests on the related resource list
            self.method_check(request, str('get'))
            return related_resource_class().get_list(request, **{related_resource_fk_field_name: kwargs['pk']})

        setattr(resource_class, view_func_name, get_related_list)

This is a mouthful, but it looks more intimidating than it is. Let's go through it step by step.

1. Function Parameters
    The function takes the same parameters our earlier mixin did, adding the base resource class in the first position.
    The mixin didn't need to know which resource class it was mixing in to, but this function does in order to call the
    ``patch_class_func`` decorator with the resource class as an argument.
2. wrap_dehydrate()
    Uses ``patch_class_func`` to add a resource URI to the returned bundle's data.  Note how it adds to the previously
    created bundle (which could come directly from Tastypie, or have been created by a user-defined ``dehydrate()``
    method on the resource), ensuring that the rest of the resource's fields remain untouched.

    One more caveat here.  In the previous two examples of building the reverse URL here, I used ``kwargs['id']`` for
    the PK of the base resource.  However, not all models' PK fields are named "id".  Here I use
    ``self._meta.object_class`` to get to the Django model this ``ModelResource`` represents, and
    ``object_class._meta.pk.name`` to find out the name of its PK field.  Now that's extensible! [3]_
3. prepend_urls()
    Instead of building the URL from scratch, I am copying the resource's dispatch detail URL.  This will break if a
    customized version of Tastypie renames or removes this URL, but that is acceptable for now.  I then append the
    related resource name to URL (e.g. ".../recipes/") and append a ``urlpatterns`` style entry to the url list.
4. get_related_list()
    This is the "view" function which returns the related resources.  Like the previous ones, it allows only the GET
    method :html_entity:`mdash` in my opinion, it doesn't make sense to allow updates or deletes on a related-resources
    list.  The only difference between this and the mixin is this function has a generic name (``get_related_list``)
    since it will be added to the resource class under its correct name (``view_func_name``) via ``setattr`` one line
    below.

Putting It All Together
=======================

All that remains is to call the ``add_related_uri_to_resource`` function on our previously defined resources.

.. code-block:: python

    from tastypie import resources, fields

    class DessertCategoryResource(resources.ModelResource):
        name = fields.CharField(attribute='name')
        ...

    class DessertRecipeResource(resources.ModelResource):
        category = fields.ForeignKey(DessertCategoryResource, 'category_parent')
        name = fields.CharField(attribute='name')
        recipe_text = fields.TextField(attribute='recipe_text')
        ...

    add_related_uri_to_resource(DessertCategoryResource, 'recipes', DessertRecipeResource, 'category')

Now let's go look at our categories:

.. code-block:: json

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects":  [
            {
                "name": "Pies",
                "recipe_uri": "/api/v1/category/1/recipes/"
                "resource_uri": "/api/v1/category/1/",
            },
            {
                "name": "Cakes",
                "recipe_uri": "/api/v1/category/2/recipes/"
                "resource_uri": "/api/v1/category/2/",
            }
        ]
    }

and our API now tells the user exactly where to find the full list of recipes for each category!  The recipe list URI
and the data available there are the same as in the hardcoded example above, but we can now use this function to add
this pattern to any ``ModelResource`` class.


Wrapping Up
===========

This was a long one!  Thanks for sticking with it.  It took longer than usual since we covered monkeypatching class
methods without overriding them in addition to adding related resource URIs. If you have any questions or fixes, you may
as always leave them in the comments.

The final code from this article is also available as a Gist_.

Footnotes
---------

.. [1] Yes, I have tasty pie on the brain.  Blame `Daniel Lindsley <https://github.com/toastdriven>`_ for coming up with
       the name.

.. [2] For simplicity, I am not displaying the models underlying these resources.  Their structure should be inferrable
       from the model field names given in the resource field names.  For example,
       ``category = fields.ForeignKey(DessertCategoryResource, 'category_parent')`` implies that the ``DessertRecipe``
       model has a ``ForeignKey`` to ``DessertCategory`` named ``category_parent``.

.. [3] Except that I still have the ``api_name`` hardcoded, meaning this will break as soon as I upgrade my API to
       v2, or use this in an API with a name other than "v1".  This is why `Jeff Atwood's version of the Rule of Three
       <http://www.codinghorror.com/blog/2013/07/rule-of-three.html>`_ states that you should use a component in at
       least three unrelated projects before you declare it reusable.  This is fixed in the Gist_ and is as easy as
       ``self._meta.api_name`` but I am leaving it here as evidence of my shame.

.. _Gist: https://gist.github.com/professorplumb/6037003