from django.template import Context, Template

def _get_detail_template():
    return Template('Hello')

def as_detail_html(instance):
    """
    Template filter that returns the given instance as a template-formatted
    block.  Inserts two objects into the context:
      ``instance`` - The model instance
      ``fields`` - A list of (name, value)-pairs representing the instance's
                    fields
    """
    template = _get_detail_template()
    fields = [(field.verbose_name, getattr(instance, field.name)) 
              for field in instance._meta.fields]
    context = Context({'instance':instance, 'fields':fields})
    return template.render(context)
