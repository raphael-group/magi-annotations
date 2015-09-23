from django import template

register = template.Library()

@register.inclusion_tag('count_tooltip.html')
def count_tooltip(name, items, placement, case=None, default='Unknown'):
    processed_items = []
    for item in items:
        val = item['val']
        if val is None or val == '': val = default
        elif case == 'upper': val = val.upper()
        elif case == 'lower': val = val.lower()
        processed_items.append( dict(val=val, count=item['count'], total=item['total']))
    return {'name': name, 'items': processed_items, 'placement': placement, default: default}

@register.simple_tag
def ref_link(identifier, db):
    link = ''
    if db == 'PMID':
        link = 'http://www.ncbi.nlm.nih.gov/pubmed/{}'.format(identifier)
    elif db == 'PMC':
        link = 'http://www.ncbi.nlm.nih.gov/pmc/articles/PMC{}/'.format(identifier)
    return "<a href='{}' target='_new'>{} {}</a>".format(link, db, identifier)
