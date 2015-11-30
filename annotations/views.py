from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.db.models import Count, Q
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.forms import inlineformset_factory

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
    context = dict(references=references, gene=gene_name, mapper=modelChoiceMappers, path=request.path)
    return render(request, 'annotations/gene.html', context)

@login_required
def saveMutation(request):
    MutRefFormSet = inlineformset_factory(Mutation, Reference, form=ReferenceForm,
                                          extra=1,can_delete=False)
    RefAnnoFormSet = inlineformset_factory(Reference, Annotation, form=AnnotationForm,
                                           extra=1,can_delete=False)

    if request.method == 'GET':
        initialMutation, initialReference, initialAnnotation = dict(), dict(), dict()
        for field in request.GET: # convert cgi params to initialize model
            # todo: have caners use abbrevs as natural key to resolve cancers from strings rather than pks
            if field in MutationForm.Meta.fields:
                initialMutation[field] = request.GET[field]
            elif field in ReferenceForm.Meta.fields:
                initialReference[field] = request.GET[field]
            elif field in AnnotationForm.Meta.fields:
                initialAnnotation[field] = request.GET[field]

        context = dict(path=request.path,
                       mutation_form=MutationForm(initial=initialMutation),
                       reference_form=MutRefFormSet(initial=[initialReference]),
                       anno_form=RefAnnoFormSet(initial=[initialAnnotation]))
        return render(request, 'annotations/createAnnotation.html', context)

    elif request.method == 'POST':
        mutationForm = MutationForm(request.POST)
        referenceFormSet = MutRefFormSet(request.POST, request.FILES)
        annotationFormSet = RefAnnoFormSet(request.POST, request.FILES)

        validMutation = None
        if mutationForm.is_valid():
            validMutation = mutationForm.save()
        elif mutationForm.non_field_errors().as_text() == "* Mutation is not unique.":
            validMutation = Mutation.getExact(mutationForm.cleaned_data)

        if validMutation:
             # only the first reference form is important
            referenceFormSet = MutRefFormSet(request.POST, request.FILES,
                                             instance=validMutation)
            refForm = referenceFormSet.extra_forms[0]

            validRef = None
            if refForm.is_valid(): 
                validRef = refForm.save(commit=False)
                validRef.source = 'Community'
                validRef.save()
            elif refForm.non_field_errors().as_text() == "* Reference is not unique.":
                validRef = Reference.getExact(refForm.cleaned_data)

            if validRef:
                annotationFormSet = RefAnnoFormSet(request.POST, request.FILES,
                                                   instance=validRef)
                if annotationFormSet.is_valid():
                    annos = annotationFormSet.save()
                    # todo: respond to ajax request instead
                    return redirect('annotations:gene', gene_name=validMutation.gene)

        # some save was invalid along the way
        originalFormContext = dict(path=request.path,
                                   mutation_form = mutationForm,
                                   reference_form = referenceFormSet,
                                   anno_form = annotationFormSet)
        return render(request, 'annotations/createAnnotation.html', originalFormContext)

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

def list_interactions(request, gene_names):
    # if there is only one, list all, else list only those included
    gene_list = gene_names.split(',')
    if len(gene_list) > 1:
        interxns = Interaction.objects.filter(source__in=gene_list, target__in=gene_list)
    elif len(gene_list) == 1:
        gene = gene_names
        interxns = Interaction.objects.filter(Q(source=gene) | Q(target=gene) )

    context = dict(interactions = interxns,
                   gene_list = gene_list,
                   path=request.path,
                   user=request.user)

    return render(request, 'annotations/interactions.html', context)

@login_required
def add_interactions(request):
    if request.method == 'GET':
        base_form =  InteractionForm(initial = {'input_source': 'Community'})
        context = dict(path = request.path,
                       user = request.user,
                       interaction_form = base_form)
        return render(request, 'annotations/add_interaction.html', context)

    elif request.method == 'POST':
        interaction_form = InteractionForm(request.POST)
        interxn = []
        if interaction_form.is_valid():
            interxn = interaction_form.save(commit = False)
            interxn.save()
        elif interaction_form.non_field_errors().as_text() == '* Interaction is not unique.':
            interxn = Interaction.getExact(interaction_form.cleaned_data)
                       
        if interxn:
            # todo: if the gene is not known, then insert it?
            # this is an issue only when editable fields are made
            ref_id = interaction_form.cleaned_data['reference_identifier']
            if ref_id:
                # look for an existing reference first
                if not InteractionReference.objects.filter(identifier = ref_id,
                                                           interaction = interxn):
                    attached_ref = InteractionReference(identifier=ref_id,
                                                    interaction = interxn,
                                                    user = request.user)                
                    attached_ref.save()

            return redirect('annotations:list_interactions', interxn.source.name + ',' + interxn.target.name)
            
        return render(request, 'annotations/add_interaction.html',
                      dict(path = request.path,
                           user = request.user,
                           interaction_form = interaction_form))

@login_required
def vote_interaction_ref(request):
    # add votes on interactions - should always be pos
    if request.method == 'POST':
        this_ref = InteractionReference.objects.get(id=request.POST.get('refId'));
        this_interxn = this_ref.interaction;

        vote_direction = request.POST.get('is_positive') == 'true'
        vote = InteractionVote(user = request.user,
                               reference = this_ref,
                               is_positive = vote_direction)
        try:
            vote.save()
        except IntegrityError as err: # todo: check specifically for duplicate error
            existing_vote = InteractionVote.objects.get(user = request.user,
                               reference = this_ref)
            existing_vote.is_positive = vote_direction
            existing_vote.save()

    # redirect to the referring page
    return redirect('annotations:list_interactions', this_interxn.source.name + ',' + this_interxn.target.name)
