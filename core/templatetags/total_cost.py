# farmers/templatetags/total_cost.py

from django import template

register = template.Library()

@register.filter
def calculate_total_cost(inventory):
    return inventory.quantity * inventory.unitPrice
