from django.template import Context, Library
from django.template.loader import get_template

from model_nodes import ModelDetailNode, ModelTeaserNode, ModelListNode

register = Library()

@register.filter
def as_detail_block(instance, title=None):
    """
    Template filter that returns the given instance as a template-formatted
    block.  Inserts two objects into the context:
      ``instance`` - The model instance
      ``fields`` - A list of (name, label, value) tuples representing the 
                   instance's fields
    """
    node = ModelDetailNode(instance)
    return node.render(Context({'title':title}))


@register.filter
def as_teaser_block(instance, title=None):
    """
    Template filter that returns the given instance as a template-formatted
    teaser.  Inserts two objects into the context:
      ``instance`` - The model instance
      ``fields`` - A list of (name, label, value) tuples representing the 
                   instance's fields
    """
    node = ModelTeaserNode(instance)
    return node.render(Context({'title':title}))


@register.filter
def as_list_block(queryset, list_title=None):
    """
    Template filter that returns the given instance list as a template-formatted
    block.  Inserts into the context:
        ``instance_list`` - The list of instances
    """
    node = ModelListNode(queryset)
    return node.render(Context({'title':list_title}))
    
