from django import template
from collections import Counter
register = template.Library()

@register.inclusion_tag('count_tooltip.html')
def count_tooltip(name, dictionary, placement, case=None, default='Unknown', mapper=dict()):
    # Create a list of each (key, value) pair:
    # 1) Mapping the key to a new name (if necessary).
    # 2) Sorting the pairs descending by value.
    items = []
    for val, count in dictionary.iteritems():
        val = mapper.get(val, val)
        if val is None or val == '': val = default
        elif case == 'upper': val = mapper.get(val, val).upper()
        elif case == 'lower': val = mapper.get(val, val).lower()
        items.append( dict(val=val, count=count) )

    items.sort(key=lambda (k, v): v, reverse=True)

    # Pass the context to the template
    context = dict(name=name, items=items, placement=placement, default=default, total=sum( dictionary.values()) )
    return context

@register.simple_tag
def majority_link_attrs(counters):
    majority = dict( (attr, '') for attr in counters)
    majority.update( (attr, Counter(counter).most_common(1)[0][0]) for attr, counter in counters.iteritems() if len(counter) > 0 )
    return ' '.join("{}='{}'".format(k, v) for k, v in majority.iteritems())

@register.simple_tag
def ref_link(identifier, db):
    link = ''
    if db == 'PMID':
        link = 'http://www.ncbi.nlm.nih.gov/pubmed/{}'.format(identifier)
    elif db == 'PMC':
        link = 'http://www.ncbi.nlm.nih.gov/pmc/articles/PMC{}/'.format(identifier)
    return "<a href='{}' target='_new'>{} {}</a>".format(link, db, identifier)
