from django import forms
from .models import ProjetRecherche
from members.models import Profile  

class ProjetRechercheForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),  
        required=True
    )

    class Meta:
        model = ProjetRecherche
        fields = ['titre', 'photo', 'problematique', 'methode_recherche', 'members', 'domaines_application', 'resultats_impacts', 'resumé']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
                'placeholder': 'Titre du projet'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full mb-3'
            }),
            'problematique': forms.Textarea(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
                'placeholder': 'Problématique',
                'rows': 4
            }),
            'methode_recherche': forms.Textarea(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
                'placeholder': 'Méthode de recherche',
                'rows': 4
            }),
            'domaines_application': forms.TextInput(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
                'placeholder': 'Domaines d\'application'
            }),
            'resultats_impacts': forms.Textarea(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
                'placeholder': 'Résultats et impacts',
                'rows': 4
            }),
            'resumé': forms.Textarea(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
                'placeholder': 'Résumé',
                'rows': 4
            }),
        }