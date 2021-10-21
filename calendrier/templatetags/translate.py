from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def translate(tex):
    tex = tex.replace("January", "Janvier", 1)
    tex = tex.replace("February", "Février", 1)
    tex = tex.replace("March", "Mars", 1)
    tex = tex.replace("April", "Avril", 1)
    tex = tex.replace("May", "Mai", 1)
    tex = tex.replace("June", "Juin", 1)
    tex = tex.replace("July", "Juillet", 1)
    tex = tex.replace("August", "Août", 1)
    tex = tex.replace("September", "Septembre", 1)
    tex = tex.replace("October", "Octobre", 1)
    tex = tex.replace("November", "Novembre", 1)
    tex = tex.replace("December", "Décembre", 1)
    tex = tex.replace("Mon", "Lun", 1)
    tex = tex.replace("Tue", "Mar", 1)
    tex = tex.replace("Wed", "Mer", 1)
    tex = tex.replace("Thu", "Jeu", 1)
    tex = tex.replace("Fri", "Ven", 1)
    tex = tex.replace("Sat", "Sam", 1)
    tex = tex.replace("Sun", "Dim", 1)
    return mark_safe(tex)
