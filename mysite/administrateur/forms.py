from django import forms
from .models import Title, ExpertiseField

class TitleCreationForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ('name',)

class ExpertiseFieldForm(forms.ModelForm):
    class Meta:
        model = ExpertiseField
        fields = ('name',)