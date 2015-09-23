from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^save/$', views.save, name='save'),
    url(r'^(?P<gene_name>[A-Za-z0-9]+)/$', views.gene, name='gene'),
    url(r'^details/(?P<ref_pk>[0-9]+)/$', views.details, name='details'),
    url(r'^save/(?P<annotation_pk>[0-9]+)/$', views.save, name='update'),
    url(r'^plus_one/(?P<gene_name>[A-Za-z0-9]+)/$', views.plus_one, name='plus_one'),
    url(r'^remove_annotation/(?P<gene_name>[A-Za-z0-9]+)/(?P<ref_pk>[0-9]+)/$', views.remove_annotation, name='remove_annotation')
]
