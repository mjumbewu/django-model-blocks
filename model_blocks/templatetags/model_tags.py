from django.template import Library, TemplateSyntaxError

from model_nodes import ModelDetailNode, ModelTeaserNode, ModelListNode

register = Library()

@register.tag
def detail_block(parser, token):
    """
    Template tag that takes a model instance and returns the given instance as 
    a template-formatted block.  Inserts two objects into the context:
      ``instance`` - The model instance
      ``fields`` - A list of (name, label, value) tuples representing the 
                   instance's fields
    
    You would want to use the tag instead of the filter primarily because, with
    a tag you can override the default template used for a particular model.
    For example, in the example project, Pepulators have Jambs, so when we put
    a detail block of a Pepulator on a page, a list of Jambs will show up.  Say
    we don't want the default detail of jambs to display; say we want a custom
    Jamb detail template.  Then we can say the following:
    
        {% with pepulator_factory_jamb_detail_template="pepulator_factory/jamb_detail.html" %}
            {% detail_block pepulator %}
        {% endwith %}
    
    The custom template is named by the app name (``pepulator_factory``), the 
    model name in all lowercase (``jamb``) and the suffix ``_template``.
    """
    try:
        tag_name, instance_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r tag requires exactly two arguments" % 
                                  token.contents.split()[0])
    
    node = ModelDetailNode(instance_name, resolved=False)
    return node


@register.tag
def teaser_block(parser, token):
    """
    Template tag that takes a model instance and returns the given instance as 
    a template-formatted block.  Inserts two objects into the context:
      ``instance`` - The model instance
      ``fields`` - A list of (name, label, value) tuples representing the 
                   instance's fields
    
    You would want to use the tag instead of the filter primarily because, with
    a tag you can override the default template used for a particular model.
    For example, in the example project, Pepulators have Jambs, so when we put
    a detail block of a Pepulator on a page, a list of Jambs will show up.  Say
    we don't want the default detail of jambs to display; say we want a custom
    Jamb detail template.  Then we can say the following:
    
        {% with pepulator_factory_jamb_teaser_template="pepulator_factory/jamb_detail.html" %}
            {% teaser_block pepulator %}
        {% endwith %}
    
    The custom template is named by the app name (``pepulator_factory``), the 
    model name in all lowercase (``jamb``) and the suffix ``_template``.
    """
    try:
        tag_name, instance_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r tag requires exactly two arguments" % 
                                  token.contents.split()[0])
    
    node = ModelTeaserNode(instance_name, resolved=False)
    return node
    

@register.tag
def list_block(parser, token):
    """
    Template tag that takes a model instance manager and returns the given 
    instances as a list in a template-formatted block.  Inserts two objects 
    into the context:
      ``model`` - The name of the model for the list
      ``instance_list`` - An iterable of model instances.
    
    You would want to use the tag instead of the filter primarily because, with
    a tag you can override the default template used for a particular model.
    For example, in the example project, Pepulators have Jambs, so when we put
    a detail block of a Pepulator on a page, a list of Jambs will show up.  Say
    we don't want the default detail of jambs to display; say we want a custom
    Jamb detail template.  Then we can say the following:
    
        {% with pepulator_factory_jamb_template="pepulator_factory/jamb_detail.html" %}
            {% detail_block pepulator %}
        {% endwith %}
    
    The custom template is named by the app name (``pepulator_factory``), the 
    model name in all lowercase (``jamb``) and the suffix ``_template``.
    """
    try:
        tag_name, list_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r tag requires exactly two arguments" % 
                                  token.contents.split()[0])
    
    node = ModelListNode(list_name, resolved=False)
    return node

