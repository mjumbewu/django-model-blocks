from django.db.models.manager import Manager
from django.template import Context, Template, Library
from django.template.loader import get_template

register = Library()

@register.filter
def as_detail_html(instance, title=None):
    """
    Template filter that returns the given instance as a template-formatted
    block.  Inserts two objects into the context:
      ``instance`` - The model instance
      ``fields`` - A list of (name, label, value) tuples representing the 
                   instance's fields
    """
    template = get_template('object_detail.html')
    
    fields = []
    for field in instance._meta.fields:
        name = field.name
        label = field.verbose_name
        value = getattr(instance, field.name)
        is_list = False
        is_direct = True
        model = instance._meta.module_name
        
        if value is not None:
            fields.append((
                name, label, value, is_list, is_direct, model,
            ))
    
    for rel_obj, model in instance._meta.get_all_related_objects_with_model():
        name = rel_obj.get_accessor_name()
        label = name
        value = getattr(instance, name)
        is_list = isinstance(value, (list, tuple, Manager))
        is_direct = False
        
        if value is not None:
            fields.append((
                name, label, value, is_list, is_direct, model,
            ))
    context = Context({'model':instance._meta.module_name, 'instance':instance, 'fields':fields, 'title':title})
    return template.render(context)


@register.filter
def as_list_html(queryset, list_title=None):
    """
    Template filter that returns the given instance list as a template-formatted
    block.  Inserts into the context:
        ``instance_list`` - The list of instances
    """
    template = get_template('object_list.html')
    
    if hasattr(queryset, 'model') and queryset.model:
        model = queryset.model._meta.module_name
    else:
        model = None
    
    context = Context({'model':model, 'instance_list':queryset, 'title':list_title})
    return template.render(context)
    
