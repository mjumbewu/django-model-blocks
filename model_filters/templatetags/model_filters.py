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
    
    fields = [(field.name, 
               field.verbose_name,
               getattr(instance, field.name),
              ) 
              for field in instance._meta.fields
              if getattr(instance, field.name) is not None]
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
    
