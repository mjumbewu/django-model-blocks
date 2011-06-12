====================
Django Model Filters
====================

The ``model_filters`` app provides you with automatically generated, stylable
generic Django templates. It fills a gap left by ``admin`` and ``databrowse`` by
providing filters that allow your to painlessly create templates with the
following properties:

* Automatically generated read-only views
* Can conform to whatever URL structure you want
* Can be placed as blocks on to your existing templates
* Integrate well with the rest of your project

Add this to the top of any template::

    {% load model_filters %}

And drop the filter anywhere you have a model instance (e.g., DetailViews)::

    {{ object|as_detail_html }}

Quick Reference
---------------

Installing
~~~~~~~~~~

You can install the ``model_filters`` app from PyPI::

    $ pip install django-model-filters

Settings
~~~~~~~~

Modify your ``INSTALLED_APPS`` setting to include::

    ...
    model_filters,
    ...

If you plan on overriding any of ``model_filter``'s default templates, remember
that ``app_directories.Loader`` searches apps in the order they are specified
in ``INSTALLED_APPS``.

Usage
~~~~~

Near the top of any template you want to use model filters, or in a base 
template, include the following line::

    {% load model_filters %}

Then, where you want to drop a generic model template, use::

    {{ object|as_detail_html }}

Or::

    {{ object_list|as_list_html }}

By default, the title on an object detail block will be the unicode
representation of the object, and the title on a list will be the name of the
model appended with `' List'`. To change the title, pass in a parameter::

    {{ object|as_detail_html:"My Special Object" }}

Help Out
--------

Found a bug? File an issue at `Github
<https://github.com/mjumbewu/django-model-filters>`. Have an improvement? Fork
it and add it, or if you can’t code it, contact us to do it.

Development
~~~~~~~~~~~

Download the code and then::

    $ pip install -r requirements.txt
    
Running Tests
~~~~~~~~~~~~~

Even simple packages need tests::

    $ python tests.py --with-coverage --cover-package=model_filters

Run it before and after you make any changes.  Try to not let that number drop.
