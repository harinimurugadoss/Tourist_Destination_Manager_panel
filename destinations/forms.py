from django import forms
from django.forms import inlineformset_factory
from .models import Destination, DestinationImage

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['place_name', 'weather', 'state', 'district', 'google_map_link', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# Formset for handling multiple images
DestinationImageFormSet = inlineformset_factory(
    Destination, 
    DestinationImage, 
    fields=('image', 'caption'),
    extra=3,
    max_num=10,
    can_delete=True
)