from django.template import Library

from model_filters import as_detail_block, as_teaser_block, as_list_block
from model_tags import detail_block, teaser_block, list_block

register = Library()

register.tag(detail_block)
register.tag(teaser_block)
register.tag(list_block)
register.filter(as_detail_block)
register.filter(as_teaser_block)
register.filter(as_list_block)

