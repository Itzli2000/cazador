from django import template

register = template.Library()


@register.simple_tag
def instance_of(instance):
    return instance.__class__.__name__
