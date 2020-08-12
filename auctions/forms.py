from django.forms import ModelForm
from .models import Listing
from django import forms

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('__all__')