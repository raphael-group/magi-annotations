from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^save/$', views.save, name='save'),
    url(r'^(?P<gene_name>[A-Za-z0-9]+)/$', views.gene, name='gene'),
    url(r'^save/mutation/$', views.saveMutation, name='saveMutation'),
    url(r'^create/mutation/$', views.saveMutation, name='createMutation'),
    url(r'^details/(?P<ref_pk>[0-9]+)/$', views.details, name='details'),
    url(r'^save/(?P<annotation_pk>[0-9]+)/$', views.save, name='update'),
    url(r'^plus_one/(?P<gene_name>[A-Za-z0-9]+)/$', views.plus_one, name='plus_one'),

    url(r'^remove_annotation/(?P<gene_name>[A-Za-z0-9]+)/(?P<ref_pk>[0-9]+)/$', views.remove_annotation, name='remove_annotation'),
    url(r'^remove_reference/(?P<ref_pk>[0-9]+)/$', views.remove_reference, name='remove_reference'),

    url(r'^interactions/add/$', views.add_interactions, name='add_interactions'),
    url(r'^interactions/vote/$', views.vote_interaction_ref, name='vote_interactions'),
    url(r'^interactions/vote/(?P<vote_id>[0-9]+)/delete$', views.remove_interaction_vote, name='remove_interaction_vote'), # todo: use REST semantics and DELETE method, with middleware
    url(r'^interactions/(?P<gene_names>[A-Za-z0-9,]+)/$', views.list_interactions, name='list_interactions'),

    url(r'^metadata/genes/all/$', views.list_genes_as_json, name='list_genes')
]
