from django import forms
from django.forms import ModelForm, Textarea
from .models import *

def validate_gene(val):
    if Gene.objects.filter(name=val).count() > 0:
        return True
    else:
        raise ValidationError(_('Gene %(value)s not known'),
                                code='Unknown',
                                params = {'value': val})
class GeneField(forms.CharField):
    default_validators = [validate_gene]

    def clean(self, value):
        cleaned_data = super(GeneField, self).clean(value)
        return Gene.objects.get(name=cleaned_data)

    
# todo: use genefield here as well
class MutationForm(ModelForm):
    class Meta:
        model = Mutation
        fields = ['gene','mutation_class', 'mutation_type', 'original_amino_acid', 'locus', 'new_amino_acid']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s is not unique.",
                }
            }

class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        fields = ['db', 'mutation', 'identifier']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s is not unique.",
                }
            }

class AnnotationForm(ModelForm):
    class Meta:
        model = Annotation
        fields = [ 'cancer', 'heritable', 'measurement_type', 'characterization', 'comment']
        widgets = { 'comment': Textarea(attrs={'cols': 40, 'rows': 3, 'class': 'form-control'})}
        

class InteractionForm(ModelForm):
    reference_identifier = forms.CharField(max_length=40)
    source = GeneField()
    target = GeneField()
    
    class Meta:
        model = Interaction
        fields = ['source', 'target', 'input_source']
        widgets = {'input_source': forms.HiddenInput()}
        
        # todo: sortable, editable field listings with a typeahead field
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': '%(model_name)s is not unique.'
            }
        }
            
