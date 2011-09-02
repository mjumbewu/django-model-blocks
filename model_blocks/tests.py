"""
Test the model blocks
"""

import datetime

from django.test import TestCase
from mock import Mock

from django.db.models import Model, IntegerField, DateTimeField, CharField
from django.template import Context, Template, TemplateSyntaxError

from example_project.pepulator_factory.models import Pepulator, Distributor
from model_blocks.templatetags import model_filters
from model_blocks.templatetags import model_nodes

class DetailBlockFilterTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_nodes.get_template = Mock(
            return_value=Template(('{{ title|default_if_none:instance|safe }}:{{ model|safe }},'
                                   '{% for name, label, value, is_list, is_link in fields %}'
                                     '{{ name|safe }},'
                                     '{{ label|safe }},'
                                     '{% if not is_list %}'
                                       '{% if is_link %}'
                                         '@{{ value }}'
                                       '{% else %}'
                                         '{{ value|safe }}'
                                       '{% endif %}'
                                     '{% else %}'
                                       '[{% for item in value.all %}{{ item|safe }},{% endfor %}]'
                                     '{% endif %},'
                                   '{% endfor %}')))
    
    
    def test_model_format(self):
        """Tests that a given model is formatted as expected."""
        pepulator = Pepulator.objects.get(serial_number=1235)
        
        expected_detail = (u"Pepulator #1235:pepulator,"
            "serial_number,serial number,1235,"
            "height,height,12,"
            "width,width,15,"
            "manufacture_date,manufacture date,2011-06-10 11:12:33,"
            "color,color,red,"
            "address,address,@ppr://1235/,"
            "distributed_by,distributed by,Walmart,"
            "knuckles,knuckles,[Knuckle of hardness 2.35,Knuckle of hardness 1.10,],"
            "jambs,jambs,[],"
        )
        detail = model_filters.as_detail_block(pepulator)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_detail.html')
        self.assertEqual(detail, expected_detail)
    
    
    def test_filter_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulator|as_detail_block }}'))
        
        pepulator = Pepulator.objects.get(serial_number=1235)
        context = Context({'pepulator':pepulator})
        
        expected_detail = (u"Pepulator #1235:pepulator,"
            "serial_number,serial number,1235,"
            "height,height,12,"
            "width,width,15,"
            "manufacture_date,manufacture date,2011-06-10 11:12:33,"
            "color,color,red,"
            "address,address,@ppr://1235/,"
            "distributed_by,distributed by,Walmart,"
            "knuckles,knuckles,[Knuckle of hardness 2.35,Knuckle of hardness 1.10,],"
            "jambs,jambs,[],"
        )
        detail = template.render(context)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_detail.html')
        self.assertEqual(detail, expected_detail)
    
    
    def test_title_is_used(self):
        """Test that a title is used if provided"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulator|as_detail_block:"My Pepulator" }}'))
        
        pepulator = Pepulator.objects.get(serial_number=1235)
        context = Context({'pepulator':pepulator})
        
        expected_detail = (u"My Pepulator:pepulator,"
            "serial_number,serial number,1235,"
            "height,height,12,"
            "width,width,15,"
            "manufacture_date,manufacture date,2011-06-10 11:12:33,"
            "color,color,red,"
            "address,address,@ppr://1235/,"
            "distributed_by,distributed by,Walmart,"
            "knuckles,knuckles,[Knuckle of hardness 2.35,Knuckle of hardness 1.10,],"
            "jambs,jambs,[],"
        )
        detail = template.render(context)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_detail.html')
        self.assertEqual(detail, expected_detail)


    def test_related_fields(self):
        """Tests that related fields not defined on the model are included."""
        pepulator = Distributor.objects.get(name="Mom & Pop")
        
        expected_detail = (u"Mom & Pop:distributor,"
            "name,name,Mom & Pop,"
            "capacity,capacity,175,"
            "stock,stock,[Pepulator #1238,],"
        )
        detail = model_filters.as_detail_block(pepulator)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_detail.html')
        self.assertEqual(detail, expected_detail)
    
    
class TeaserBlockFilterTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_nodes.get_template = Mock(
            return_value=Template('{{ title|default_if_none:instance|safe }}:{{ model|safe }},{% for name, label, value, is_list in fields %}{{ name|safe }},{{ label|safe }},{% if not is_list %}{{ value|safe }}{% else %}[{% for item in value.all %}{{ item|safe }},{% endfor %}]{% endif %},{% endfor %}'))
    
    
    def test_model_format(self):
        """Tests that a given model is formatted as expected."""
        pepulator = Pepulator.objects.get(serial_number=1235)
        
        expected_teaser = (u"Pepulator #1235:pepulator,"
            "serial_number,serial number,1235,"
            "height,height,12,"
            "width,width,15,"
            "manufacture_date,manufacture date,2011-06-10 11:12:33,"
            "color,color,red,"
            "address,address,ppr://1235/,"
            "distributed_by,distributed by,Walmart,"
            "knuckles,knuckles,[Knuckle of hardness 2.35,Knuckle of hardness 1.10,],"
            "jambs,jambs,[],"
        )
        teaser = model_filters.as_teaser_block(pepulator)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_teaser.html')
        self.assertEqual(teaser, expected_teaser)
    
    
class ListBlockFilterTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_nodes.get_template = Mock(
            return_value=Template('{{ title|default_if_none:model|capfirst }}{% if not title %}s{% endif %}:{{ instance_list|safe }}'))
    
    
    def test_list_format(self):
        """Tests that a given model is formatted as expected."""
        pepulator_list = Pepulator.objects.filter(serial_number__gt=2000)
        
        expected_rendering = (u"Pepulators:[<Pepulator: Pepulator #2345>, "
                               "<Pepulator: Pepulator #2346>]")
        rendering = model_filters.as_list_block(pepulator_list)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_list.html')
        self.assertEqual(rendering, expected_rendering)
    
    
    def test_filter_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulators|as_list_block }}'))
        pepulator_list = Pepulator.objects.filter(serial_number__gt=2000)
        context = Context({'pepulators':pepulator_list})
        
        expected_rendering = (u"Pepulators:[<Pepulator: Pepulator #2345>, "
                               "<Pepulator: Pepulator #2346>]")
        rendering = template.render(context)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_list.html')
        self.assertEqual(rendering, expected_rendering)

    
    def test_empty_queryset(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulators|as_list_block }}'))
        pepulator_list = Pepulator.objects.filter(serial_number__gt=5000)
        context = Context({'pepulators':pepulator_list})
        
        expected_rendering = (u"Pepulators:[]")
        rendering = template.render(context)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_list.html')
        self.assertEqual(rendering, expected_rendering)

    
    def test_non_query_set_results_in_no_model(self):
        """Test that when a non queryset is used, the model is None"""
        # Why? Because we try to read the model off of the queryset. If we just
        # have a list of objects, then we don't know the model.
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulators|as_list_block }}'))
        pepulator_list = [p for p in Pepulator.objects.filter(serial_number__gt=2000)]
        context = Context({'pepulators':pepulator_list})
        
        expected_rendering = (u"Nones:[<Pepulator: Pepulator #2345>, "
                               "<Pepulator: Pepulator #2346>]")
        rendering = template.render(context)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_list.html')
        self.assertEqual(rendering, expected_rendering)

    
    def test_empty_list(self):
        """Test that when a non queryset is used, the model is None"""
        
        template = Template(('{% load model_filters %}'
                             '{{ pepulators|as_list_block }}'))
        pepulator_list = []
        context = Context({'pepulators':pepulator_list})
        
        expected_rendering = (u"Nones:[]")
        rendering = template.render(context)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_list.html')
        self.assertEqual(rendering, expected_rendering)

    
    def test_alternate_title_is_used(self):
        """Test that a list title is used if provided"""
        template = Template(('{% load model_filters %}'
                             '{{ pepulators|as_list_block:"Some Pepulators" }}'))
        pepulator_list = Pepulator.objects.filter(serial_number__gt=2000)
        context = Context({'pepulators':pepulator_list})
        
        expected_rendering = (u"Some Pepulators:[<Pepulator: Pepulator #2345>, "
                               "<Pepulator: Pepulator #2346>]")
        rendering = template.render(context)
        
        model_nodes.get_template.assert_called_with('model_blocks/object_list.html')
        self.assertEqual(rendering, expected_rendering)


class DetailBlockTagTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_nodes.get_template = Mock(
            return_value=Template('{{ title|default_if_none:instance|safe }}:{{ model|safe }},{% for name, label, value, is_list in fields %}{{ name|safe }},{{ label|safe }},{% if not is_list %}{{ value|safe }}{% else %}[{% for item in value.all %}{{ item|safe }},{% endfor %}]{% endif %},{% endfor %}'))
    
    
    def test_tag_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_tags %}'
                             '{% with pepulator_factory_pepulator_detail_template="pepulator_factory/pepulator_detail.html" %}'
                             '{% detail_block pepulator %}'
                             '{% endwith %}'))
        
        pepulator = Pepulator.objects.get(serial_number=1235)
        context = Context({'pepulator':pepulator})
        
        expected_detail = (u"Pepulator #1235:pepulator,"
            "serial_number,serial number,1235,"
            "height,height,12,"
            "width,width,15,"
            "manufacture_date,manufacture date,2011-06-10 11:12:33,"
            "color,color,red,"
            "address,address,ppr://1235/,"
            "distributed_by,distributed by,Walmart,"
            "knuckles,knuckles,[Knuckle of hardness 2.35,Knuckle of hardness 1.10,],"
            "jambs,jambs,[],"
        )
        detail = template.render(context)
        
        model_nodes.get_template.assert_called_with('pepulator_factory/pepulator_detail.html')
        self.assertEqual(detail, expected_detail)
    
    
    def test_with_specific_fields(self):
        """Test that the included fields spec is respected"""
        
        template = Template(('{% load model_tags %}'
                             '{% with pepulator_factory_pepulator_detail_template="pepulator_factory/pepulator_detail.html" %}'
                             '{% with pepulator_factory_pepulator_fields="serial_number, color, height, width" %}'
                             '{% detail_block pepulator %}'
                             '{% endwith %}'
                             '{% endwith %}'))
        
        pepulator = Pepulator.objects.get(serial_number=1235)
        context = Context({'pepulator':pepulator})
        
        expected_detail = (u"Pepulator #1235:pepulator,"
            "serial_number,serial number,1235,"
            "color,color,red,"
            "height,height,12,"
            "width,width,15,"
        )
        detail = template.render(context)
        
        self.assertEqual(detail, expected_detail)
    
    
    def test_with_excluded_fields(self):
        """Test that the excluded fields spec is respected"""
        
        template = Template(('{% load model_tags %}'
                             '{% with pepulator_factory_pepulator_detail_template="pepulator_factory/pepulator_detail.html" %}'
                             '{% with pepulator_factory_pepulator_exclude="knuckles, jambs, color, address" %}'
                             '{% detail_block pepulator %}'
                             '{% endwith %}'
                             '{% endwith %}'))
        
        pepulator = Pepulator.objects.get(serial_number=1235)
        context = Context({'pepulator':pepulator})
        
        expected_detail = (u"Pepulator #1235:pepulator,"
            "serial_number,serial number,1235,"
            "height,height,12,"
            "width,width,15,"
            "manufacture_date,manufacture date,2011-06-10 11:12:33,"
            "distributed_by,distributed by,Walmart,"
        )
        detail = template.render(context)
        
        self.assertEqual(detail, expected_detail)
    
    
    def test_fail_on_wrong_number_of_arguments(self):
        self.assertRaises(TemplateSyntaxError, Template, 
                          ('{% load model_tags %}'
                           '{% detail_block pepulator "overflow" %}'))
        self.assertRaises(TemplateSyntaxError, Template, 
                          ('{% load model_tags %}'
                           '{% detail_block %}'))
    
    
class TeaserBlockTagTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_nodes.get_template = Mock(
            return_value=Template('{{ title|default_if_none:instance|safe }}:{{ model|safe }},{% for name, label, value, is_list in fields %}{{ name|safe }},{{ label|safe }},{% if not is_list %}{{ value|safe }}{% else %}[{% for item in value.all %}{{ item|safe }},{% endfor %}]{% endif %},{% endfor %}'))
    
    
    def test_tag_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_tags %}'
                             '{% with pepulator_factory_pepulator_teaser_template="pepulator_factory/pepulator_teaser.html" %}'
                             '{% teaser_block pepulator %}'
                             '{% endwith %}'))
        
        pepulator = Pepulator.objects.get(serial_number=1235)
        context = Context({'pepulator':pepulator})
        
        expected_teaser = (u"Pepulator #1235:pepulator,"
            "serial_number,serial number,1235,"
            "height,height,12,"
            "width,width,15,"
            "manufacture_date,manufacture date,2011-06-10 11:12:33,"
            "color,color,red,"
            "address,address,ppr://1235/,"
            "distributed_by,distributed by,Walmart,"
            "knuckles,knuckles,[Knuckle of hardness 2.35,Knuckle of hardness 1.10,],"
            "jambs,jambs,[],"
        )
        teaser = template.render(context)
        
        model_nodes.get_template.assert_called_with('pepulator_factory/pepulator_teaser.html')
        self.assertEqual(teaser, expected_teaser)
    
    def test_fail_on_wrong_number_of_arguments(self):
        self.assertRaises(TemplateSyntaxError, Template, 
                          ('{% load model_tags %}'
                           '{% teaser_block pepulator "overflow" %}'))
        self.assertRaises(TemplateSyntaxError, Template, 
                          ('{% load model_tags %}'
                           '{% teaser_block %}'))
    
    
class ListBlockTagTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_nodes.get_template = Mock(
            return_value=Template('{{ title|default_if_none:model|capfirst }}{% if not title %}s{% endif %}:{{ instance_list|safe }}'))
    
    
    def test_filter_is_registered(self):
        """Test that the filter can be used from within a template"""
        
        template = Template(('{% load model_tags %}'
                             '{% with pepulator_factory_pepulator_list_template="pepulator_factory/pepulator_list.html" %}'
                             '{% list_block pepulators %}'
                             '{% endwith %}'))
        pepulator_list = Pepulator.objects.filter(serial_number__gt=2000)
        context = Context({'pepulators':pepulator_list})
        
        expected_rendering = (u"Pepulators:[<Pepulator: Pepulator #2345>, "
                               "<Pepulator: Pepulator #2346>]")
        rendering = template.render(context)
        
        model_nodes.get_template.assert_called_with('pepulator_factory/pepulator_list.html')
        self.assertEqual(rendering, expected_rendering)
    
    def test_fail_on_wrong_number_of_arguments(self):
        self.assertRaises(TemplateSyntaxError, Template, 
                          ('{% load model_tags %}'
                           '{% list_block pepulators "overflow" %}'))
        self.assertRaises(TemplateSyntaxError, Template, 
                          ('{% load model_tags %}'
                           '{% list_block %}'))

class ModelBlockModuleTest (TestCase):
    def test_all_tags_and_filters_loaded(self):
        template = Template(('{% load model_blocks %}'
                             '{% detail_block pepulator %}'
                             '{% list_block pepulators %}'
                             '{{ pepulator|as_detail_block }}'
                             '{{ pepulators|as_list_block }}'))
                             
        # We just care that everything loaded, and we were able to get here
        # without incidence.
        self.assert_(True)


class SideEffectsTest (TestCase):
    fixtures = ['pepulator_factory_data.json']

    def setUp(self):
        # Mock Django's get_template so that it doesn't load a real file;
        # instead just return a template that allows us to verify the context
        model_nodes.get_template = Mock(
            return_value=Template('{{ title|default_if_none:model|capfirst }}{% if not title %}s{% endif %}'))
    
    
    def test_model_doesnt_carry_over_into_future_blocks(self):
        template = Template(('{% load model_tags %}'
                             '{{ model }}'
                             '{% list_block distributors %}'
                             '{{ model }}'))
        distributor_list = Distributor.objects.all()
        context = Context({'model':'My String',
                           'distributors':distributor_list})
        
        expected_rendering = (u"My String"
                               "Distributors"
                               "My String")
        rendering = template.render(context)
        
        self.assertEqual(rendering, expected_rendering)

