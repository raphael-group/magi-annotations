from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
from django import forms
from django_bootstrap_typeahead.fields import *

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

class Gene(models.Model):
    name = models.CharField(max_length=30, primary_key = True)
    chromosome = models.CharField(max_length=2, null = True)
    locus_begin = models.IntegerField(null = True)
    locus_end = models.IntegerField(null = True)
    def __unicode__(self):
        return unicode(self.name)

class Mutation(models.Model):
    gene                = models.ForeignKey(Gene)
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

# protein-protein interactions
class Interaction(models.Model):
    source = models.ForeignKey(Gene, related_name='source')
    target = models.ForeignKey(Gene, related_name='target')
    input_source = models.CharField(max_length=25) # answers: which network does this come from?
    def __unicode__(self):
        return unicode(self.source) +  "->" +  unicode(self.target)

    class Meta:
        unique_together = (("source", "target", "input_source"))

    @staticmethod
    def getExact(inter_dict):
        return Interaction.objects.get(source = inter_dict['source'],
                                       target = inter_dict['target'],
                                       input_source = inter_dict['input_source'])

class InteractionReference(models.Model):
    identifier = models.CharField(max_length=40)
    db = models.CharField(max_length=30, choices=dbChoices) # reference source
    interaction = models.ForeignKey(Interaction)
    user = models.ForeignKey(User, null = True)
    def __unicode__(self):
        return unicode(self.identifier)

    def vote_count(self):
        upvotes = self.interactionvote_set.filter(is_positive=True)
        downvotes = self.interactionvote_set.filter(is_positive=False)
        return len(upvotes) - len(downvotes)

    class Meta:
        unique_together = (("identifier", "interaction"))

class InteractionVote(models.Model):
    user = models.ForeignKey(User, null = True)
    reference = models.ForeignKey(InteractionReference)
    is_positive = models.BooleanField()
    class Meta:
        unique_together = (("user", "reference"))

    def __unicode__(self):
        return "Vote: " + self.user.username + " -> " + ("Yes" if self.is_positive else "No") + " on " + unicode(self.reference)
