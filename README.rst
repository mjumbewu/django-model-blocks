====================
Django Model Filters
====================

The ``model_filters`` app allows you to have generic Django templates.  It fills a gap left by ``admin`` and ``databrowse`` by providing filters that allow your to painlessly create templates with the following properties:

* Automatically generated read-only views
* Can conform to whatever URL structure you want
* Can be placed as blocks on to your existing templates
* Integrate well with the rest of your project

Add this to the top of any template:

    {% load model_filters %}

And drop the filter anywhere you have a model instance (e.g., DetailViews):

    {{ object|as_detail_html }}

Running Tests
-------------

    $ python tests.py --with-coverage --cover-package=model_filters

Run it before and after you make any changes.  Try to not let that number drop.
