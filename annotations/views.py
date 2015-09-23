from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the annotations index.")

def gene(request, gene_name):
    # Get all the references for this gene name
    references  = Reference.objects.filter(mutation__gene__iexact=gene_name).order_by('identifier').order_by('mutation__locus')

    # Create a "summarized" list of annotations for each reference,
    # counting the number of distinct values for the cancer, heritable,
    # measurement_type, and characterization fields
    annotations = []
    for r in references:
        # Load the reference's annotations
        subannotations = Annotation.objects.filter(reference=r.pk)
        N = len(subannotations)

        # Initialize a new "summarized" Annotation
        A = { "mutation_class": r.mutation.mutation_class,
              "mutation_type": r.mutation.get_mutation_type_display,
              "locus": r.mutation.locus,
              "oaa": r.mutation.original_amino_acid,
              "naa": r.mutation.new_amino_acid,
              "source": r.source,
              "db": r.db,
              "identifier": r.identifier,
              "ref_pk": r.pk,
              "user_annotated": any( a for a in subannotations if a.user == request.user ),
              "no_annotations": len(subannotations) == 0
        }

        # For each of our summary fields, record the count of each
        # distinct value
        fields = [('cancer__abbr', 'cancers', None),
                   ('heritable', 'heritable', abbrToHeritable),
                   ('measurement_type', 'measurement_type', None),
                   ('characterization', 'characterization', abbrToCharacterization)]
        for field, attr_name, mapper in fields:
            counter = subannotations.values(field).annotate(count=Count(field)).order_by('-count')
            def display_name(val):
                if val == '' or val is None or mapper is None: return val
                else: return mapper[val]
            counter = [ dict(count=c['count'], val=display_name(c[field]), total=N) for c in counter ]
            # Hack to make sure that all the counts total the same amount
            totalCount = sum( c['count'] for c in counter )
            if totalCount != N:
                counter.append(dict(count=N-totalCount, val='', total=N))
            A[attr_name] = counter
        annotations.append( A )

    # Render the view
    context = dict(annotations=annotations, gene=gene_name)
    return render(request, 'annotations/gene.html', context)

def details(request, ref_pk):
    # Retrieve the annotations for this reference
    ref = Reference.objects.get(pk=ref_pk)
    annotations = Annotation.objects.filter(reference=ref)

    # Initialize the context
    context = dict(mutation=ref.mutation, ref=ref, user=request.user, annotations=annotations)

    # Retrieve the annotation for the current user (if necessary)
    if request.user.is_authenticated():
        try:
            user_annotation = Annotation.objects.get(user=request.user, reference=ref)
            context['annotation_form'] = AnnotationForm(instance=user_annotation)
            context['user_annotation'] = user_annotation
        except Annotation.DoesNotExist:
            context['annotation_form'] = AnnotationForm()
    return render(request, 'annotations/details.html', context)

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
    def valueIfValid(D, key, mapper=None):
        val = request.POST.get(key)
        if val == '' or val is None: return
        elif mapper: D[key] = mapper[val]
        else: D[key]=  val

    attrs = dict(reference=ref, user=request.user)
    valueIfValid(attrs, 'heritable', heritableToAbbr)
    valueIfValid(attrs, 'measurementType', measurementToAbbr)
    valueIfValid(attrs, 'characterization', characterizationToAbbr)
    valueIfValid(attrs, 'cancer')

    # Find the specific
    if 'cancer' in attrs:
        attrs['cancer'] = Cancer.objects.get(abbr=attrs['cancer'])

    # Add a new annotation
    ref = Reference.objects.get(pk=refPk)
    a   = Annotation(**attrs)
    a.save()

    # Redirect to the gene page in question
    return redirect('annotations:gene', gene_name=gene_name)

@login_required
def remove_annotation(request, gene_name, ref_pk):
    ref = Reference.objects.get(pk=ref_pk)
    A = Annotation.objects.get(user=request.user, reference=ref)
    A.delete()
    return redirect('annotations:gene', gene_name=gene_name)
