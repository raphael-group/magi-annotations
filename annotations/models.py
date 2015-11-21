from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
from django import forms

# CONSTANTS
mutationTypeChoices  = (('MS', 'Missense'), ('NS', 'Nonsense'), ('FSI', 'Frame-Shift Insertion'), ('IFD', 'In-Frame Deletion'), ('FSD', 'Frame-Shift Deletion'), ('IFI', 'In-Frame Insertion'))
mutationClassChoices = (('SNV', 'Single Nucleotide Variant'), ('indel', 'Small insertion/deletion'))
heritableChoices     = (('G', 'Germline'), ('S', 'Somatic'))
referenceSourceChoices = (('C', 'Community'), ('DoCM', 'Database of Curated Mutations'), ('PMC Search', 'PubMed Central Search'))
dbChoices = (('PMID', 'PubMed'), ('PMC', 'PubMed Central'))
measurementChoices = (('WXS', 'Whole-Exome Sequencing'), ('WGS', 'Whole-Genome Sequencing'), ('TS', 'Targeted Sequencing'))
characterizationChoices = (('F', 'Functional'), ('O', 'Observational'))
modelChoiceMappers = dict(measurement_type=dict(measurementChoices),
                          characterization=dict(characterizationChoices),
                          heritable=dict(heritableChoices))

# Create your models here.
class Cancer(models.Model):
    name        = models.CharField(max_length=100)
    abbr        = models.CharField(max_length=10, primary_key=True)
    color       = models.CharField(max_length=7)
    last_edited = models.DateField(auto_now=True)
    created_on  = models.DateField(auto_now_add=True)

    def __unicode__(self): return '{} ({})'.format(self.name, self.abbr)

class Mutation(models.Model):
    gene                = models.CharField(max_length=30)
    locus               = models.IntegerField('locus')
    original_amino_acid = models.CharField(max_length=30) # describes SNV
    new_amino_acid      = models.CharField(max_length=30)
    mutation_type       = models.CharField(max_length=15, choices=mutationTypeChoices)
    mutation_class      = models.CharField(max_length=15, choices=mutationClassChoices)
    last_edited         = models.DateField(auto_now=True)
    created_on          = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '{}:{}{}{} ({} {})'.format(self.gene, self.original_amino_acid, self.locus, self.new_amino_acid, self.mutation_type, self.mutation_class)

    def full_change(self):
        return self.original_amino_acid + str(self.locus) + self.new_amino_acid

    def clean(self):
        if self.locus <= 0:
            raise ValidationError({'locus': _('Locus should be positive.')})
        if self.original_amino_acid == self.new_amino_acid:
            raise ValidationError({'new_amino_acid': _('New amino acid must be different from original.')})

    @staticmethod
    def getExact(mutationDict):
        return Mutation.objects.get(
            gene=mutationDict['gene'],
            mutation_type=mutationDict['mutation_type'],
            mutation_class=mutationDict['mutation_class'],
            locus=mutationDict['locus'],
            original_amino_acid=mutationDict['original_amino_acid'],
            new_amino_acid=mutationDict['new_amino_acid'])

    class Meta:
        unique_together = (("gene","locus","original_amino_acid","new_amino_acid","mutation_type","mutation_class"))

class MutationForm(ModelForm):
    class Meta:
        model = Mutation
        fields = ['gene','mutation_class', 'mutation_type', 'original_amino_acid', 'locus', 'new_amino_acid']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s is not unique.",
                }
            }

class Reference(models.Model):
    identifier = models.CharField(max_length=30)
    db = models.CharField(max_length=30, choices=dbChoices)
    source = models.CharField(max_length=30, choices=referenceSourceChoices)
    mutation = models.ForeignKey(Mutation)
    last_edited      = models.DateField(auto_now=True)
    created_on       = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '{} {} for {} ({})'.format(self.db, self.identifier, self.mutation, self.source)

    @staticmethod
    def getExact(refDict):
        return Reference.objects.get(
            identifier=refDict['identifier'],
            db=refDict['db'],
            mutation=refDict['mutation'].pk)

    class Meta:
        unique_together = (('identifier', 'db', 'mutation'))

class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        fields = ['db', 'mutation', 'identifier']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s is not unique.",
                }
            }

class Annotation(models.Model):
    heritable        = models.CharField(max_length=8, choices=heritableChoices, blank=True, verbose_name="Heritability")
    cancer           = models.ForeignKey(Cancer, blank=True, null=True)
    measurement_type = models.CharField(max_length=30, choices=measurementChoices, blank=True)
    characterization = models.CharField(max_length=20, choices=characterizationChoices, blank=True)
    reference        = models.ForeignKey(Reference)
    user             = models.ForeignKey(User, null=True, blank=True)
    comment          = models.CharField(max_length=300, blank=True)
    last_edited      = models.DateField(auto_now=True)
    created_on       = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return 'Annotation: ' + unicode(self.reference)

    def heritable_mapped(self):
        if self.heritable in heritableChoices:
            return heritableChoices[self.heritable]
        return "Unknown"

    def measurement_mapped(self):
        if self.measurement_type in measurementChoices:
            return measurementChoices[self.measurement_type]
        return "Unknown"

    def characterization_mapped(self):
        if self.characterization in characterizationChoices:
            return characterizationChoices[self.characterization]
        return "Unknown"

class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = [ 'cancer', 'heritable', 'measurement_type', 'characterization', 'comment']
        widgets = { 'comment': Textarea(attrs={'cols': 40, 'rows': 3, 'class': 'form-control'})}

# todo: link mutations to genes
class Gene(models.Model):
    name = models.CharField(max_length=30, primary_key = True)
    chromosome = models.SmallIntegerField(null = True)
    locus = models.IntegerField(null = True)
    def __unicode__(self):
        return unicode(self.name)

# protein-protein interactions
class Interaction(models.Model):
    source = models.ForeignKey(Gene, related_name='source')
    target = models.ForeignKey(Gene, related_name='target')
    input_source = models.CharField(max_length=25)
#    user = models.ForeignKey(User, null = True)
    def __unicode__(self):
        return unicode(self.source) +  "->" +  unicode(self.target)

class InteractionReference(models.Model):
    identifier = models.CharField(max_length=40) # all references are PMIDs for the time being
    interaction = models.ForeignKey(Interaction)
    def __unicode__(self):
        return unicode(self.identifier)

class InteractionForm(ModelForm):
    reference_identifier = forms.CharField(max_length=40)
    # todo: how to make this a widget?
    class Meta:
        model = Interaction
        fields = ['source', 'target']
        # todo: sortable, editable field listings
