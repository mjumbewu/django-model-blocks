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
              for field in instance._meta.fields]
    context = Context({'instance':instance, 'fields':fields})
    return template.render(context)
