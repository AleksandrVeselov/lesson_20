from django import template

register = template.Library()


@register.simple_tag
def mediapath_tag(image):
   return f'/media/{image}'

