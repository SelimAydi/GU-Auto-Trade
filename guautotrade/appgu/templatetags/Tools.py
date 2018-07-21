from django import template

register = template.Library()

@register.filter
def stripslashes(url):
    return url.replace('/', '')