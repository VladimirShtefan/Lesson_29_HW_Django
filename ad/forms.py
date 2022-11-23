from django import forms

from ad.models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = '__all__'
