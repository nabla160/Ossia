from django import template

register = template.Library()


@register.filter
def frenchmonth(tex):
    rep = tex
    if tex == "January":
        rep = "Janvier"
    if tex == "February":
        rep = "Février"
    if tex == "March":
        rep = "Mars"
    if tex == "April":
        rep = "Avril"
    if tex == "May":
        rep = "Mai"
    if tex == "June":
        rep = "Juin"
    if tex == "July":
        rep = "Juillet"
    if tex == "August":
        rep = "Août"
    if tex == "September":
        rep = "Septembre"
    if tex == "October":
        rep = "Octobre"
    if tex == "November":
        rep = "Novembre"
    if tex == "December":
        rep = "Décembre"
    return rep
