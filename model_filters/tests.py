"""
Test the model filters
"""

import datetime

from django.test import TestCase
from mock import Mock

from django.db.models import Model, IntegerField, DateTimeField, CharField
from django.template import Context, Template

from example_project.pepulator_factory.models import Pepulator
from model_filters.templatetags import model_filters

class DetailHtmlFilterTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_filters.get_template = Mock(
            return_value=Template('{{ instance|safe }}:{{ model|safe }},{{ fields|safe }}'))
    
    
    def test_model_format(self):
        """Tests that a given model is formatted as expected."""
        pepulator = Pepulator.objects.get(serial_number=1235)
        
        expected_detail = (u"Pepulator #1235:pepulator,["
              "('serial number', 1235), "
              "('height', 12), "
              "('width', 15), "
              "('manufacture date', datetime.datetime(2011, 6, 10, 11, 12, 33)), "
              "('color', u'red'), "
              "('distributed by', <Distributor: Walmart>)"
              "]")
        detail = model_filters.as_detail_html(pepulator)
        
        model_filters.get_template.assert_called_with('object_detail.html')
        self.assertEqual(detail, expected_detail)
    
    
    def test_filter_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulator|as_detail_html }}'))
        
        pepulator = Pepulator.objects.get(serial_number=1235)
        context = Context({'pepulator':pepulator})
        
        expected_detail = (u"Pepulator #1235:pepulator,["
              "('serial number', 1235), "
              "('height', 12), "
              "('width', 15), "
              "('manufacture date', datetime.datetime(2011, 6, 10, 11, 12, 33)), "
              "('color', u'red'), "
              "('distributed by', <Distributor: Walmart>)"
              "]")
        detail = template.render(context)
        
        model_filters.get_template.assert_called_with('object_detail.html')
        self.assertEqual(detail, expected_detail)


class ListHtmlFilterTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_filters.get_template = Mock(
            return_value=Template('{{ model|capfirst }}s:{{ instance_list|safe }}'))
    
    
    def test_list_format(self):
        """Tests that a given model is formatted as expected."""
        pepulator_list = Pepulator.objects.filter(serial_number__gt=2000)
        
        expected_rendering = (u"Pepulators:[<Pepulator: Pepulator #2345>, <Pepulator: Pepulator #2346>]")
        rendering = model_filters.as_list_html(pepulator_list)
        
        model_filters.get_template.assert_called_with('object_list.html')
        self.assertEqual(rendering, expected_rendering)
    
    
    def test_filter_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulators|as_list_html }}'))
        pepulator_list = Pepulator.objects.filter(serial_number__gt=2000)
        context = Context({'pepulators':pepulator_list})
        
        expected_rendering = (u"Pepulators:[<Pepulator: Pepulator #2345>, <Pepulator: Pepulator #2346>]")
        rendering = template.render(context)
        
        model_filters.get_template.assert_called_with('object_list.html')
        self.assertEqual(rendering, expected_rendering)
