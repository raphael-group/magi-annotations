from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.db.models import Count, Q, Case, Value, When
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

# Create your views here.

def remove_extra_fields(data_dict, model_class):
    return {k: v for (k, v) in data_dict.items()
            if k in model_class._meta.get_all_field_names()}

## CREATE operations ##
@login_required
def save_annotation_only(request, annotation_pk=None): # create a single mutation reference annotation
    # Try to get the annotation and update it
    if annotation_pk is not None:
        instance = Annotation.objects.get(pk=annotation_pk)
        ref      = instance.reference
        form     = AnnotationForm(instance=instance, data=request.POST)
        # Make sure that the user is the same
        if request.user != instance.user:
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

def prefill_forms(query_params, *forms):
    initialForms = []
    for field, value in request.GET.iteritems():
        for i, form in enumerate(forms):
            if field in form.Meta.fields:
                pass
            
    return initialForms
@login_required
# create a mutation and reference and (optionally) an annotation
# todo: these should be atomic transactions
def save_mutation(request):
    # Formsets allow us to build one formset on top of another, but a compound form may be clearer
    # this will be improved in the CNA branch
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
            validMutation = Mutation.objects.get(**remove_extra_fields(mutationForm.cleaned_data, Mutation))

        if validMutation:
             # only the first reference form is important
            referenceFormSet = MutRefFormSet(request.POST, request.FILES,
                                             instance=validMutation)
            refForm = referenceFormSet.extra_forms[0]

            validRef = None
            if refForm.is_valid():
                validRef = refForm.save(commit=False)
                validRef.source = 'Community'
                validRef.user = request.user
                validRef.save()
            elif refForm.non_field_errors().as_text() == "* Reference is not unique.":
                del refForm.cleaned_data['id']
                validRef = Reference.objects.get(**remove_extra_fields(refForm.cleaned_data, Reference))

            if validRef:
                annotationFormSet = RefAnnoFormSet(request.POST, request.FILES,
                                                   instance=validRef)
                if annotationFormSet.is_valid():
                    annos = annotationFormSet.save(commit=False)
                    if annos:
                        anno = annos[0]
                        anno.user = request.user
                        anno.save()

                    # todo: respond to ajax request instead
                    return redirect('annotations:gene', gene_name=validMutation.gene)

        # some save was invalid along the way
        originalFormContext = dict(path=request.path,
                                   mutation_form = mutationForm,
                                   reference_form = referenceFormSet,
                                   anno_form = annotationFormSet)
        return render(request, 'annotations/createAnnotation.html', originalFormContext)

@login_required
# create an annotation that agrees with the majority
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
# create an interaction and reference
# todo: these should be atomic transactions
def add_interactions(request):
    if request.method == 'GET':
        initialInteraction = {'input_source': 'Community'}
        for field in request.GET:
            initialInteraction[field] = request.GET[field]

        base_form = InteractionForm(initial = initialInteraction)
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
            interxn = Interaction.objects.get(**remove_extra_fields(interaction_form.cleaned_data, Interaction))
            

        if interxn:
            ref_id = interaction_form.cleaned_data['reference_identifier'] # create
            db = interaction_form.cleaned_data['db']
            if ref_id:
                # look for an existing reference first
                # todo: consider get_or_create for this pattern
                if not InteractionReference.objects.filter(identifier = ref_id,
                                                           interaction = interxn,
                                                           db=db):
                    attached_ref = InteractionReference(identifier=ref_id,
                                                    interaction = interxn,
                                                    db = db,
                                                    user = request.user)
                    attached_ref.save()

            return redirect('annotations:list_interactions', interxn.source.name + ',' + interxn.target.name)

        return render(request, 'annotations/add_interaction.html',
                      dict(path = request.path,
                           user = request.user,
                           interaction_form = interaction_form))

@login_required
# vote on an interaction, or modify an existing interaction vote
def vote_interaction_ref(request):
    if request.method == 'POST':
        this_ref = InteractionReference.objects.get(id=request.POST.get('refId'));
        this_interxn = this_ref.interaction;

        if request.POST.get('delete') == 'true':
            try:
                existing_vote = InteractionVote.objects.get(user = request.user,
                                reference = this_ref)

                existing_vote.delete()
            except ObjectDoesNotExist: # nothing to delete
                print "Warning: Attempt to delete non-existent vote for %s, reference %s " % (request.user, this_ref.identifier)

        else:
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

        # todo: send json redirect or return to the referring page
        return redirect('annotations:list_interactions', this_interxn.source.name + ',' + this_interxn.target.name)
    else: # should never GET
        return redirect('profile')


## RETRIEVE operations
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
    refs = Reference.objects.filter(mutation__gene=gene_name).values(*fields).annotate(*counters)

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

# necessary for the typeahead code to get a list of genes
def list_genes_as_json(request):
    gene_list = map(lambda s: unicode(s), Gene.objects.values_list('name', flat=True))
    gene_list.sort()
    return JsonResponse({'genes': gene_list})

def list_interactions(request, gene_names):
    # if there is only one, list all, else list only those included
    gene_list = gene_names.split(',')
    if len(gene_list) > 1:
        interxns = Interaction.objects.filter(source__in=gene_list, target__in=gene_list)
    elif len(gene_list) == 1:
        gene = gene_names
        interxns = Interaction.objects.filter(Q(source=gene) | Q(target=gene) )

    # identify which items have a user's vote
    user_votes = {}
    if request.user.is_authenticated():
        refs_with_vote = InteractionReference.objects.filter(
            interaction__in = interxns,
            interactionvote__user = request.user)
        for ref in refs_with_vote:
            user_votes[ref.pk] = ref.interactionvote_set.get(user = request.user).is_positive

    context = dict(interactions = interxns,
                   gene_list = gene_list,
                   user_votes = user_votes,
                   path=request.path,
                   user=request.user)

    return render(request, 'annotations/interactions.html', context)

### DELETE operations
## todo: improve redirect behavior for these so that they return ajax type responses which pages absorb
@login_required
def remove_annotation(request, gene_name, ref_pk):
    ref = Reference.objects.get(pk=ref_pk)
    A = Annotation.objects.all().filter(user=request.user, reference=ref)
    A.delete()
    return redirect('annotations:gene', gene_name=gene_name)

## todo: improve redirect behavior for these so that they return ajax type responses which pages absorb
@login_required
def remove_reference(request, ref_pk):
    A = Reference.objects.get(user=request.user, pk=ref_pk)
    A.delete()
    return redirect('profile')

@login_required
def remove_interaction_vote(request, vote_id):
    this_vote = InteractionVote.objects.get(id=vote_id)
    if request.user == this_vote.user:
        this_vote.delete()
    else:
        print "WARNING: attempt to delete vote %s by non-owner %s" % (this_vote, request.user)
    # todo: send json redirect or return to the referring page
    return redirect('profile')

@login_required
def remove_interaction(request, interaction_pk):
    this_interaction = InteractionReference.objects.get(id=interaction_pk)
    if request.user == this_interaction.user:
        this_interaction.delete()
    else:
        print "WARNING: attempt to delete interaction %s by non-owner %s" % (this_interaction, request.user)
    # todo: send json redirect or return to the referring page
    return redirect('profile')
