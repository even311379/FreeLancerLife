import markdown
from django.template import Library

register = Library()

@register.filter(name='markdown')
def markdown_filter(value):
    return markdown.markdown(
        value,
        extensions=[
            'extra',
            'codehilite',
            'wagtailmd.mdx.mdx_mathjax',
        ],
        extension_configs = {
            'codehilite':[
                ('css_class',"highlight")
            ]
        },
        output_format='html5'
    )