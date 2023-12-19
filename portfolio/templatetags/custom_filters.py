from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def intcomma(value):
    try:
        value = floatformat(value, 0)
        parts = value.split(".")
        parts[0] = "{:,}".format(int(parts[0]))
        return ".".join(parts)
    except (ValueError, TypeError):
        return value