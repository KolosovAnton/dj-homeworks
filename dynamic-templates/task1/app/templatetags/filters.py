from django import template

register = template.Library()


@register.filter
def color_background(inflation_month):
    if inflation_month == '-':
        s = "#FFFFFF"
        return s
    elif float(inflation_month) < 0:
        s = "#008000"
        return s
    elif float(inflation_month) <= 1:
        s = "#FFFFFF"
        return s
    elif float(inflation_month) <= 2:
        s = "#FFDAB9"
        return s
    elif float(inflation_month) <= 5:
        s = "#FA8072"
        return s
    elif float(inflation_month) > 5:
        s = "#FF0000"
        return s
