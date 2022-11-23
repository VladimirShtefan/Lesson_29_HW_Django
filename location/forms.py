from django import forms

from location.models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
