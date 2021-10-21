from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def autotranslate(current_language, description, description_en):

    if current_language != "fr" and description_en:
        return mark_safe(description_en)
    elif current_language == "fr" and not description:
        return mark_safe(description_en)
    else:
        return mark_safe(description)
