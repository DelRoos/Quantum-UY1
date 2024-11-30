from django import forms
from .models import ProjetRecherche
from members.models import Member  


class ProjetRechercheForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Ou utilisez un autre widget si vous le souhaitez
        required=True
    )

    class Meta:
        model = ProjetRecherche
        fields = ['titre', 'problematique', 'methode_recherche', 'members', 'domaines_application', 'resultats_impacts', 'resumé']