from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse, TemplateResponse
from .models import *
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from collections import defaultdict

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the annotations index.")

def gene(request, gene_name):
    # List of fields we want to display for our references
    fields = ['mutation__mutation_class', 'mutation__mutation_type',
              'mutation__locus', 'mutation__original_amino_acid',
              'mutation__new_amino_acid', 'pk', 'identifier', 'db', 'source',
              'annotation__heritable', 'annotation__measurement_type',
              'annotation__characterization', 'annotation__cancer__abbr', 'annotation__user_id']

    # Values we want to count
    annotation_fields = ['annotation__heritable', 'annotation__measurement_type',
                         'annotation__characterization', 'annotation__cancer__abbr']
    counters = [ Count(f) for f in annotation_fields ]
    refs = Reference.objects.filter(mutation__gene__iexact=gene_name).values(*fields).annotate(*counters)

    # For each value we want to count, merge the counts across references
    pkToAnnotation = dict()
    for ref in refs:
        if ref['pk'] not in pkToAnnotation:
            ref['user_annotated'] = False
            ref['counter'] = dict( (f, defaultdict(int)) for f in annotation_fields)
            ref['no_annotations'] = True
            pkToAnnotation[ref['pk']] = ref
        if request.user.is_authenticated() and request.user.pk == ref['annotation__user_id']:
            pkToAnnotation[ref['pk']]['user_annotated'] = True
        for f in annotation_fields:
            if ref[f] == '' or ref[f] is None: continue
            pkToAnnotation[ref['pk']]['counter'][f][ref[f]] += ref[f + '__count']
            pkToAnnotation[ref['pk']]['no_annotations'] = False

    # Sort the annotations
    references = sorted(pkToAnnotation.values(), key=lambda r: (not r['user_annotated'], r['no_annotations'], r['mutation__locus']))

    # Render the view
    print "in view:"
    print request.referral_site
    context = dict(references=references, 
                   gene=gene_name, 
                   mapper=modelChoiceMappers, 
                   path=request.path)
    
    return TemplateResponse(request, 'annotations/gene.html', context=context)

def details(request, ref_pk):
    # Retrieve the annotations for this reference
    ref = Reference.objects.get(pk=ref_pk)
    annotations = Annotation.objects.filter(reference=ref)

    # Initialize the context
    context = dict(mutation=ref.mutation, ref=ref, user=request.user, annotations=annotations, path=request.path)

    # Retrieve the annotation for the current user (if necessary)
    if request.user.is_authenticated():
        try:
            user_annotation = Annotation.objects.get(user=request.user, reference=ref)
            context['annotation_form'] = AnnotationForm(instance=user_annotation)
            context['user_annotation'] = user_annotation
        except Annotation.DoesNotExist:
            context['annotation_form'] = AnnotationForm()
    return TemplateResponse(request, 'annotations/details.html', context=context)

@login_required
def save(request, annotation_pk=None):
    # Try to get the annotation and update it
    if annotation_pk is not None:
        instance = Annotation.objects.get(pk=annotation_pk)
        ref      = instance.reference
        form     = AnnotationForm(instance=instance, data=request.POST)
        # Make sure that the
        if request.user.pk != instance.user.pk:
            return redirect('annotations:details', ref_pk=ref.pk)

    # Otherwise we're making a new annotation
    else:
        ref  = Reference.objects.get(pk=request.POST.get('reference_id'))
        form = AnnotationForm(data=request.POST)

    # Try saving the form
    if form.is_valid():
        a = form.save(commit=False)
        a.reference = ref
        a.user = request.user
        a.save()
    else:
        print form.errors

    return redirect('annotations:details', ref_pk=ref.pk)

@login_required
def plus_one(request, gene_name):
    # Extract the reference we're annotating
    refPk = int(request.POST.get('refPk'))
    ref   = Reference.objects.get(pk=refPk)

    # Parse the post request
    attrs = dict(reference=ref, user=request.user)
    def valueIfValid(key, newKey):
        val = request.POST.get(key)
        if val == '' or val is None: return
        else: attrs[newKey]=  val

    valueIfValid('annotation__heritable', 'heritable')
    valueIfValid('annotation__measurement_type', 'measurement_type')
    valueIfValid('annotation__characterization', 'characterization')
    valueIfValid('annotation__cancer__abbr', 'cancer')

    # Find the specific
    if 'cancer' in attrs:
        attrs['cancer'] = Cancer.objects.get(abbr=attrs['cancer'])

    # Add a new annotation
    a   = Annotation(**attrs)
    a.save()

    # Redirect to the gene page in question
    return redirect('annotations:gene', gene_name=gene_name)

@login_required
def remove_annotation(request, gene_name, ref_pk):
    ref = Reference.objects.get(pk=ref_pk)
    A = Annotation.objects.all().filter(user=request.user, reference=ref)
    A.delete()
    return redirect('annotations:gene', gene_name=gene_name)
