from django.db.models.manager import Manager
from django.template import Context, Node, Variable
from django.template.loader import get_template

class ModelDetailNode (Node):
    def __init__(self, model_inst, resolved=True):
        self.instance = model_inst
        self.resolved = resolved
        
    def get_context_data(self):
        fields = []
        for field in self.instance._meta.fields:
            name = field.name
            label = field.verbose_name
            value = getattr(self.instance, field.name)
            is_list = False
            is_direct = True
            model = self.instance._meta.module_name
            
            if value is not None:
                fields.append((
                    name, label, value, is_list, is_direct, model,
                ))
        
        for rel_obj, model in self.instance._meta.get_all_related_objects_with_model():
            name = rel_obj.get_accessor_name()
            label = name
            value = getattr(self.instance, name)
            is_list = isinstance(value, (list, tuple, Manager))
            is_direct = False
            
            if value is not None:
                fields.append((
                    name, label, value, is_list, is_direct, model,
                ))
        
        return {'model':self.instance._meta.module_name, 
                'instance':self.instance, 
                'fields':fields}
    
    def get_template_variable(self):
        template_variable = '%s_%s_template' % \
            (self.instance._meta.app_label, self.instance._meta.module_name)
        return template_variable
    
    def render(self, context):
        if not self.resolved:
            self.instance = Variable(self.instance).resolve(context)
        
        template_variable = self.get_template_variable()
        template_name = context.get(template_variable,
                                    'model_filters/object_detail.html')
        template = get_template(template_name)
        
        context.update(Context(self.get_context_data()))
        return template.render(context)


class ModelListNode (Node):
    def __init__(self, model_list, resolved=True):
        self.queryset = model_list
        
    def get_context_data(self):
        if hasattr(self.queryset, 'model') and self.queryset.model:
            model = self.queryset.model._meta.module_name
        else:
            model = None
        
        return {'model':model, 'instance_list':self.queryset}
    
    def get_template_variable(self):
        return ''
    
    def render(self, context):
        template_variable = self.get_template_variable()
        template_name = context.get(template_variable,
                                    'model_filters/object_list.html')
        template = get_template(template_name)
        
        context.update(Context(self.get_context_data()))
        return template.render(context)



