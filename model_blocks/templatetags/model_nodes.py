from django.db.models.manager import Manager
from django.template import Context, Node, Variable
from django.template.loader import get_template

class BaseModelBlockNode (Node):
    def __init__(self, thing, resolved=True):
        """
        thing -- The thing (probably a model instance or a list of model 
                 instances) to be rendered as a block.
        resolved -- If True, then ``thing`` is a resolved value.  If False,
                    then thing is the name of a variable which, in context,
                    will contain the value of the thing.
        """
        self.thing = thing
        self.resolved = resolved
    
    def get_template_variable(self, thing, type_of_thing):
        """
        Return the name of the template variable that should be used to render
        the thing.  If the variable name does not resolve to a value, then a 
        default template will be used.
        """
        if isinstance(thing, (list, tuple)):
            template_variable = ''
        elif hasattr(thing, 'model') and thing:
            template_variable = '%s_%s_%s_template' % \
                (thing.model._meta.app_label, thing.model._meta.module_name, 
                 type_of_thing)
        elif hasattr(thing, '_meta') and thing:
            template_variable = '%s_%s_%s_template' % \
                (thing._meta.app_label, thing._meta.module_name, type_of_thing)
        else:
            template_variable = ''
        return template_variable
    
    def get_resolved_value(self, context):
        """
        Return a resolved version of the thing being rendered -- either a model
        instance or a list of such instances. Specifically, if the name of the
        value was passed to the node as a string, resolve the value w.r.t. the
        context. If the actual value was passed in, then just return the value. 
        """
        if not self.resolved:
            res_var = Variable(self.thing).resolve(context)
        else:
            res_var = self.thing
        return res_var
    
    def render(self, context):
        # Grab the thing to render.  It'll be a model instance, or a queryset,
        # or a list or something.
        thing = self.get_resolved_value(context)
        
        # Get the name of the context variable that holds the override template
        # file name.
        template_variable = self.get_template_variable(thing, self.thing_type)
        
        # If the override template file name is set, then use that.  Otherwise,
        # use the default template for the thing type
        template_name = context.get(template_variable,
                                    'model_blocks/object_%s.html' % self.thing_type)
        template = get_template(template_name)
        
        # Get the data necessary for rendering the thing, and add it to the
        # context.
        context.update(Context(self.get_context_data(thing, context)))
        
        # The variable 'title' must be in the context.  If it's not there, add
        # it and set it to None
        if 'title' not in context:
            context['title'] = None
        
        # After rendering, pop off of the context so that it's back to normal 
        # for the next tag.
        rendering = template.render(context)
        context.pop()
        return rendering


class ModelDetailNode (BaseModelBlockNode):
    
    thing_type = 'detail'
    
    def __get_fields_list_variable(self, instance, var_suffix):
        # The variable name is built up from the name of the app, the name of 
        # the model, and the specified suffix.
        fields_list_variable = '%s_%s_%s' % \
            (instance._meta.app_label, instance._meta.module_name, var_suffix)
        
        return fields_list_variable
        
    
    def __get_field_list(self, instance, context, var_suffix):
        # Get the variable name to look for
        var = self.__get_fields_list_variable(instance, var_suffix)
        fields_str = context.get(var, None)
        
        # If the variable is not set, just return an empty list
        if fields_str is None:
            return []
        
        # If the variable is set, split the list on comma (,) and return
        else:
            include_fields = [field.strip() for field in fields_str.split(',')]
            return include_fields
            
    
    def get_include_fields(self, instance, context):
        """Return a list of fields and order to include in the rendering."""
        return self.__get_field_list(instance, context, 'fields')
        
    
    def get_exclude_fields(self, instance, context):
        """Return a list of fields to exclude from the rendering."""
        return self.__get_field_list(instance, context, 'exclude')
        
    
    def get_context_data(self, instance, context):
        """
        Calculate additional context data that will be used to render the thing.
        
        """
        include_fields = self.get_include_fields(instance, context)
        exclude_fields = self.get_exclude_fields(instance, context)
        
        fields = []
        for field in instance._meta.fields:
            name = field.name
            
            if name in exclude_fields:
                continue
            
            if include_fields and name not in include_fields:
                continue
            
            label = field.verbose_name
            value = getattr(instance, field.name)
            is_list = False
            is_link = (type(field).__name__ in ('URLField',))
            model = instance._meta.module_name
            
            if value is not None:
                fields.append((
                    name, label, value, is_list, is_link, model,
                ))
        
        for rel_obj, model in instance._meta.get_all_related_objects_with_model():
            name = rel_obj.get_accessor_name()
            
            if name in exclude_fields:
                continue
            
            if include_fields and name not in include_fields:
                continue
            
            label = name
            value = getattr(instance, name)
            is_list = isinstance(value, (list, tuple, Manager))
            is_link = False
            
            if value is not None:
                fields.append((
                    name, label, value, is_list, is_link, model,
                ))
        
        # If include_fields was defined, then sort by the order.
        if include_fields:
            fields = sorted(fields, key=lambda field: include_fields.index(field[0]))
                
        
        return {'model':instance._meta.module_name, 
                'instance':instance, 
                'fields':fields}


class ModelTeaserNode (ModelDetailNode):
    
    thing_type = 'teaser'


class ModelListNode (BaseModelBlockNode):
    
    thing_type = 'list'
    
    def get_context_data(self, queryset, context):
        if hasattr(queryset, 'model') and queryset.model:
            model = queryset.model._meta.module_name
        else:
            model = None
        
        return {'model':model, 'instance_list':queryset}
    

