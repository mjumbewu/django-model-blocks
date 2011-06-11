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

    def setUp(self):
        # Create a model instance
        now = datetime.datetime.now()
        self.m = Pepulator(
            serial_number = 123456,
            height = 25,
            width = 16,
            manufacture_date = now,
            color = 'chartreuse',
        )
        
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_filters.get_template = Mock(
            return_value=Template('{{ instance|safe }}:{{ fields|safe }}'))
    
    
    def test_model_format(self):
        """Tests that a given model is formatted as expected."""
        
        expected_detail = (u"Pepulator #123456:[('serial number', 123456),"
              " ('height', 25), ('width', 16), ('manufacture date', %r),"
              " ('color', 'chartreuse')]") % self.m.manufacture_date
        detail = model_filters.as_detail_html(self.m)
        
        model_filters.get_template.assert_called_with('object_detail.html')
        self.assertEqual(detail, expected_detail)
    
    
    def test_filter_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulator|as_detail_html }}'))
        context = Context({'pepulator':self.m})
        
        expected_detail = (u"Pepulator #123456:[('serial number', 123456),"
            " ('height', 25), ('width', 16), ('manufacture date', %r),"
            " ('color', 'chartreuse')]") % self.m.manufacture_date
        detail = template.render(context)
        
        model_filters.get_template.assert_called_with('object_detail.html')
        self.assertEqual(detail, expected_detail)


class ListHtmlFilterTest (TestCase):

    def setUp(self):
        # Create a model instance
        now = datetime.datetime.now()
        self.l = [
            Pepulator(
                serial_number = 123456,
                height = 25,
                width = 16,
                manufacture_date = now,
                color = 'chartreuse',
            ),
            Pepulator(
                serial_number = 987654,
                height = 25,
                width = 16,
                manufacture_date = now,
                color = 'grey',
            ),
            Pepulator(
                serial_number = 246810,
                height = 25,
                width = 16,
                manufacture_date = now,
                color = 'sunset',
            ),
        ]
        
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_filters.get_template = Mock(
            return_value=Template('Pepulators:{{ instance_list|safe }}'))
    
    
    def test_list_format(self):
        """Tests that a given model is formatted as expected."""
        
        expected_rendering = (u"Pepulators:%r" % self.l)
        rendering = model_filters.as_list_html(self.l)
        
        model_filters.get_template.assert_called_with('object_list.html')
        self.assertEqual(rendering, expected_rendering)
    
    
    def test_filter_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulators|as_list_html }}'))
        context = Context({'pepulators':self.l})
        
        expected_rendering = (u"Pepulators:%r" % self.l)
        rendering = template.render(context)
        
        model_filters.get_template.assert_called_with('object_list.html')
        self.assertEqual(rendering, expected_rendering)
