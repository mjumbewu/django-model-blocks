from django.template import Context, Template, Library
from django.template.loader import get_template

register = Library()

@register.filter
def as_detail_html(instance):
    """
    Template filter that returns the given instance as a template-formatted
    block.  Inserts two objects into the context:
      ``instance`` - The model instance
      ``fields`` - A list of (name, value)-pairs representing the instance's
                   fields
    """
    template = get_template('object_detail.html')
    fields = [(field.verbose_name, getattr(instance, field.name)) 
              for field in instance._meta.fields
              if getattr(instance, field.name) is not None]
    context = Context({'instance':instance, 'fields':fields})
    return template.render(context)


@register.filter
def as_list_html(queryset):
    """
    Template filter that returns the given instance list as a template-formatted
    block.  Inserts into the context:
        ``instance_list`` - The list of instances
    """
    template = get_template('object_list.html')
    context = Context({'instance_list':queryset})
    return template.render(context)
    
