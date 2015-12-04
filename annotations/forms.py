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

### set up gene fields to be typehaead autocomplete fields
class GeneWidget(forms.TextInput):    
    def __init__(self, *args, **kwargs):
        if 'attrs' not in kwargs:
            kwargs['attrs'] = {'class': 'gene-typeahead'}
        elif 'class' not in kwargs['attrs']:
            kwargs['attrs']['class'] = 'gene-typeahead'
        else:
            kwargs['attrs']['class'] += ' gene-typeahead'
              
        super(forms.TextInput, self).__init__(*args, **kwargs)
        
### note: in the template, the form's media must be included in scripts block
    class Media:
        js = ('components/d3/d3.min.js',
              'components/typeahead.js/dist/typeahead.bundle.min.js',
              'components/handlebars/handlebars.min.js',
              'components/gene-typeahead.js',)

class GeneField(forms.CharField):
    description = "typeahead field for selecting genes"

    ### note: by validating this way, we only accept annotations for genes we know about
    default_validators = [validate_gene]
    widget = GeneWidget
    
    def clean(self, value):
        cleaned_data = super(GeneField, self).clean(value)
        return Gene.objects.get(name=cleaned_data)
    
class MutationForm(ModelForm):
    gene = GeneField()  
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
    db = forms.CharField(max_length=20,
                         widget = forms.Select(choices=dbChoices))
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
            
