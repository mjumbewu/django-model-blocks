from django.template import Library

from model_filters import as_detail_html, as_list_html
from model_tags import detail_block, list_block

register = Library()

register.tag(detail_block)
register.tag(list_block)
register.filter(as_detail_html)
register.filter(as_list_html)

