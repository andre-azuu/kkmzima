from django import template

register = template.Library()

@register.filter
def sum_total_costs(inventory_list):
    total_expenses = sum(inventory.total_cost for inventory in inventory_list)
    return total_expenses