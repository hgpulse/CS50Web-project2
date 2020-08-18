from django.forms import ModelForm, SelectDateWidget, TextInput
from .models import Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('__all__')
        widgets = {
            'name': TextInput(attrs={'placeholder':'Title'}),
            'description': TextInput(attrs={'placeholder':'Description'}),
            'initial_price': TextInput(attrs={'placeholder':'Price'}),
            'date': SelectDateWidget()
        }



