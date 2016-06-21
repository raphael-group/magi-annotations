from django import template

register = template.Library()

# your filters here
@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
