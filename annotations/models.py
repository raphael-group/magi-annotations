from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea

# CONSTANTS
mutationTypeChoices  = (('MS', 'Missense'), ('NS', 'Nonsense'), ('FSI', 'Frame-Shift Insertion'), ('IFD', 'In-Frame Deletion'), ('FSD', 'Frame-Shift Deletion'), ('IFI', 'In-Frame Insertion'))
abbrToMutationType   = dict(mutationTypeChoices)
mutationClassChoices = (('SNV', 'Single Nucleotide Variant'), ('indel', 'Small insertion/deletion'))
abbrToMutationClass  = dict(mutationClassChoices)
heritableChoices     = (('G', 'Germline'), ('S', 'Somatic'))
abbrToHeritable      = dict(heritableChoices)
heritableToAbbr      = dict( (v, k) for k, v in abbrToHeritable.iteritems() )
referenceSourceChoices = (('C', 'Community'), ('DoCM', 'Database of Curated Mutations'), ('PMC Search', 'PubMed Central Search'))
abbrToSource = dict(referenceSourceChoices)
dbChoices = (('PMID', 'PubMed'), ('PMC', 'PubMed Central'))
abbrToDb = dict(dbChoices)
measurementChoices = (('WXS', 'Whole-Exome Sequencing'), ('WGS', 'Whole-Genome Sequencing'), ('TS', 'Targeted Sequencing'))
abbrToMeasurement = dict(measurementChoices)
measurementToAbbr = dict( (v, k) for k, v in abbrToMeasurement.iteritems() )
characterizationChoices = (('F', 'Functional'), ('O', 'Observational'))
abbrToCharacterization = dict(characterizationChoices)
characterizationToAbbr = dict( (v, k) for k, v in abbrToCharacterization.iteritems() )

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
    original_amino_acid = models.CharField(max_length=30)
    new_amino_acid      = models.CharField(max_length=30)
    mutation_type       = models.CharField(max_length=15, choices=mutationTypeChoices)
    mutation_class      = models.CharField(max_length=15, choices=mutationClassChoices)
    last_edited         = models.DateField(auto_now=True)
    created_on          = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '{}:{}{}{} ({} {})'.format(self.gene, self.original_amino_acid, self.locus, self.new_amino_acid, self.mutation_type, self.mutation_class)

class Reference(models.Model):
    identifier = models.CharField(max_length=30)
    db = models.CharField(max_length=30, choices=dbChoices)
    source = models.CharField(max_length=30, choices=referenceSourceChoices)
    mutation = models.ForeignKey(Mutation)
    last_edited      = models.DateField(auto_now=True)
    created_on       = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '{} {} for {} ({})'.format(self.db, self.identifier, self.mutation, self.source)

class Annotation(models.Model):
    heritable        = models.CharField(max_length=8, choices=heritableChoices, blank=True)
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

class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = ['heritable', 'cancer', 'measurement_type', 'characterization', 'comment']
        widgets = { 'comment': Textarea(attrs={'cols': 40, 'rows': 3, 'class': 'form-control'})}
