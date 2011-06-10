"""
Test the model filters
"""

import datetime

from django.test import TestCase
from mock import Mock

from django.db.models import Model, IntegerField, DateTimeField, CharField
from django.template import Context, Template
from model_filters.templatetags import model_filters

class DetailHtmlFilterTest (TestCase):

    def setUp(self):
        # Create a sample model
        class PepulatorModel (Model):
            serial_number = IntegerField(primary_key=True)
            height = IntegerField()
            width = IntegerField()
            manufacture_date = DateTimeField()
            color = CharField(max_length=32)
        
            def __unicode__(self):
                return u'Pepulator #%s' % self.serial_number
        
        # Create a model instance
        now = datetime.datetime.now()
        self.m = PepulatorModel(
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
