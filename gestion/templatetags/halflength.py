from math import ceil

from django.template import Library

register = Library()


@register.filter
def half_length(liste):
    try:
        return ceil(len(liste) / 2)
    except (ValueError, ZeroDivisionError):
        return None
