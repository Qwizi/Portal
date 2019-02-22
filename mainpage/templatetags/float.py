from django import template
from django.conf import settings

register = template.Library()

@register.filter
def make_cash(value):
    return float(value)