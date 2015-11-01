from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag
def node_magi_url(path, referer):
    if referer:
        return "{}{}".format(referer, path)
    else:
        return "{}{}".format(settings.__getattr__('NODE_MAGI_URL'), path)
