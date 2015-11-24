from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='has_errors')
def has_errors(form):
    return len(form.errors) > 0 and not isinstance(form.errors, list)
