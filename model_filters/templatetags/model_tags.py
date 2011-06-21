from django.db.models.manager import Manager
from django.template import Context, Template, Library, Node
from django.template.loader import get_template

# Import the filters so that they're available when doing `load model_tags`
from model_filters import *

register = Library()


