from django.db.models.manager import Manager
from django.template import Context, Template, Library, Node
from django.template.loader import get_template

from model_nodes import ModelDetailNode, ModelListNode

register = Library()

@register.tag
def detail_block(parser, token):
    pass
