from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    try:
        return range(int(number))
    except (ValueError, TypeError):
        return range(0)
