from django.template import Context, Template, Library
from django.template.loader import get_template
from django.contrib.contenttypes.models import ContentType

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
    content_type = ContentType.objects.get_for_model(instance)
    
    fields = [(field.name, 
               field.verbose_name,
               getattr(instance, field.name),
              ) 
              for field in instance._meta.fields
              if getattr(instance, field.name) is not None]
    context = Context({'model':content_type.model, 'instance':instance, 'fields':fields, 'title':title})
    return template.render(context)


@register.filter
def as_list_html(queryset, list_title=None):
    """
    Template filter that returns the given instance list as a template-formatted
    block.  Inserts into the context:
        ``instance_list`` - The list of instances
    """
    template = get_template('object_list.html')
    
    if queryset.model:
        content_type = ContentType.objects.get_for_model(queryset.model)
        model = content_type.model
    else:
        model = 'object'
    
    context = Context({'model':model, 'instance_list':queryset, 'title':list_title})
    return template.render(context)
    
