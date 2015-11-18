from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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
    abbr        = models.CharField(max_length=10)
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
        if original_amino_acid == new_amino_acid:
            raise ValidationError({'new_amino_acid': _('New amino acid must be different from original.')})

class MutationForm(ModelForm):
    class Meta:
        model = Mutation
        fields = ['gene','locus', 'original_amino_acid','new_amino_acid', 'mutation_type', 'mutation_class']

class Reference(models.Model):
    identifier = models.CharField(max_length=30)
    db = models.CharField(max_length=30, choices=dbChoices)
    source = models.CharField(max_length=30, choices=referenceSourceChoices)
    mutation = models.ForeignKey(Mutation)
    last_edited      = models.DateField(auto_now=True)
    created_on       = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '{} {} for {} ({})'.format(self.db, self.identifier, self.mutation, self.source)

class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        fields = ['db', 'mutation', 'identifier']

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
