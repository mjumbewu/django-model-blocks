from django.db.models.manager import Manager
from django.template import Context, Template, Library, Node
from django.template.loader import get_template

register = Library()

class ModelDetailNode (Node):
    def __init__(self, model_inst, alternate_template_name):
        self.instance = model_inst
        self.template_name = alternate_template_name
        
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
    
    def render(self, context):
        if self.template_name in context:
            template = get_template(self.template_name)
        else:
            template = get_template('model_filters/object_detail.html')
        
        context.update(
            Context(self.get_context_data())
        )
        return template.render(context)


@register.filter
def as_detail_html(instance, title=None):
    """
    Template filter that returns the given instance as a template-formatted
    block.  Inserts two objects into the context:
      ``instance`` - The model instance
      ``fields`` - A list of (name, label, value) tuples representing the 
                   instance's fields
    """
    node = ModelDetailNode(instance, 'asdkjagdsa')
    return node.render(Context({'title':title}))


@register.filter
def as_list_html(queryset, list_title=None):
    """
    Template filter that returns the given instance list as a template-formatted
    block.  Inserts into the context:
        ``instance_list`` - The list of instances
    """
    template = get_template('model_filters/object_list.html')
    
    if hasattr(queryset, 'model') and queryset.model:
        model = queryset.model._meta.module_name
    else:
        model = None
    
    context = Context({'model':model, 'instance_list':queryset, 'title':list_title})
    return template.render(context)
    
