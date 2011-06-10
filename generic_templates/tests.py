"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime

from django.test import TestCase
from mock import Mock

from django.db.models import Model, IntegerField, DateTimeField, CharField
from django.template import Context, Template
from generic_templates.templatetags import generic_filters as gf

class DetailHtmlFilterTest (TestCase):
    def test_model_format(self):
        """
        Tests that a given model is formatted as expected.
        """
        class PepulatorModel (Model):
            serial_number = IntegerField(primary_key=True)
            height = IntegerField()
            width = IntegerField()
            manufacture_date = DateTimeField()
            color = CharField(max_length=32)
        
            def __unicode__(self):
                return u'Pepulator #%s' % self.serial_number
        
        now = datetime.datetime.now()
        m = PepulatorModel(
            serial_number = 123456,
            height = 25,
            width = 16,
            manufacture_date = now,
            color = 'chartreuse',
        )
        
        gf.get_template = Mock(return_value=Template('{{ instance|safe }}:{{ fields|safe }}'))
        
        expected_detail = u"Pepulator #123456:[('serial number', 123456), ('height', 25), ('width', 16), ('manufacture date', %r), ('color', 'chartreuse')]" % m.manufacture_date
        detail = gf.as_detail_html(m)
        
        gf.get_template.assert_called_with('object_detail.html')
        self.assertEqual(detail, expected_detail)
