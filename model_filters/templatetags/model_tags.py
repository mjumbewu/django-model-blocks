from django.template import Library, TemplateSyntaxError

from model_nodes import ModelDetailNode, ModelListNode

register = Library()

@register.tag
def detail_block(parser, token):
    try:
        tag_name, instance_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r tag requires exactly two arguments" % 
                                  token.contents.split()[0])
    
    node = ModelDetailNode(instance_name, resolved=False)
    return node

