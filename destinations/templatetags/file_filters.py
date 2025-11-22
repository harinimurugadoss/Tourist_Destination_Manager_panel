from django import template
from django.template.defaultfilters import filesizeformat

register = template.Library()

@register.filter
def human_readable_size(value):
    """Convert file size to human-readable format."""
    return filesizeformat(value)