from django import template

register = template.Library()

@register.filter
def first_image(destination):
    """Return the first image of a destination or None."""
    return destination.images.first()

@register.filter
def remaining_images(destination):
    """Return all images except the first one."""
    return destination.images.all()[1:]