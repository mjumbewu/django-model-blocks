====================
Django Model Blocks
====================

The ``model_blocks`` app provides you with automatically generated, stylable
generic Django model template partials. It fills a gap left by ``admin`` and
``databrowse`` by providing filters and tags that allow your to painlessly
create templates with the following properties:

* Automatically generated read-only views
* Can conform to whatever URL structure you want
* Can be placed as blocks on to your existing templates
* Integrate well with the rest of your project

Add this to the top of any template::

    {% load model_blocks %}

And drop the filter anywhere you have a model instance (e.g., DetailViews)::

    {{ object|as_detail_block }}

Quick Reference
---------------

Installing
~~~~~~~~~~

You can install the ``model_blocks`` app from PyPI::

    $ pip install django-model-blocks

Settings
~~~~~~~~

Modify your ``INSTALLED_APPS`` setting to include::

    ...
    model_blocks,
    ...

Basic Usage
~~~~~~~~~~~

Near the top of any template you want to use model blocks, or in a base 
template, include the following line::

    {% load model_blocks %}

Then, where you want to drop a generic model template, use::

    {{ object|as_detail_block }}

Or::

    {{ object_list|as_list_block }}

(**NOTE:** If your list has many objects, consider using pagination, as the list 
may require a long time to render.)

By default, the title on an object detail block will be the unicode
representation of the object, and the title on a list will be the name of the
model appended with `' List'`. To change the title, pass in a parameter::

    {{ object|as_detail_block:"My Special Object" }}

Advanced Usage
~~~~~~~~~~~~~~

While using the filters remains the original and most simple way to render
the blocks, if you want/need greater control over the specifics of how certain
models render, you can use the tag notation::

    {% detail_block object %}

    {% list_block object_list %}

You can still override the title by using ``with``::

    {% with title="My Special Object" %}
        {% detail_block object %}
    {% endwith %}

Yeah, if all you need to do is override the title, then stick with the filters.  
However, When you drop a detail block into your template, it will automatically 
render all of the referenced object's fields, including related model fields.  
This potentially results in a tree of objects in your page.  The tag notation's 
strength is revealed when you need to use a custom template for any model in 
your tree.

The ``example_project`` in the source includes a demonstration of this feature.
In that example, there are ``Pepulator`` objects, and each one may have several 
``Knuckle`` objects and several ``Jamb`` objects.  However, each ``Knuckle`` has 
a field referring to the URL of an image.  On our ``Pepulator`` detail page, we 
want all of our ``Kuckle`` objects and ``Jamb`` objects shown.  The default 
template is sufficient for ``Jamb`` objects, but we have to provide a custom 
template (based on the default) for each ``Knuckle``.  So, we render the 
``Pepulator`` detail like so::

    {% with pepulator_factory_knuckle_detail_template="pepulator_factory/knuckle_detail.html" %}
        {% detail_block pepulator %}
    {% endwith %}

Voila!  For more information, check out the 
`pepulator_detail.html <https://github.com/mjumbewu/django-model-blocks/blob/master/example_project/pepulator_factory/templates/pepulator_factory/pepulator_detail.html>`_ 
and 
`knuckle_detail.html <https://github.com/mjumbewu/django-model-blocks/blob/master/example_project/pepulator_factory/templates/pepulator_factory/knuckle_detail.html>`_ 
files.

Help Out
--------

Found a bug? File an issue at `Github
<https://github.com/mjumbewu/django-model-blocks>`_. Have an improvement? Fork
it and add it, or if you can’t code it, File an `issue
<https://github.com/mjumbewu/django-model-blocks>`_ and we'll do it.

Are you using or thinking of using ``django-model-filters``?  Please `drop a 
line <https://github.com/inbox/new/mjumbewu>`_ and let us know what for.  
Knowing how people use it in the wild will help us make it better!

Development
~~~~~~~~~~~

Download the code and then::

    $ pip install -r requirements.txt
    
Running Tests
~~~~~~~~~~~~~

Even simple packages need tests::

    $ python tests.py --with-coverage --cover-package=model_block

Run it before and after you make any changes.  Try to not let that number drop.
