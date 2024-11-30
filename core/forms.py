from django import forms
from .models import Contact, Newsletter

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre message'})
        }
    
class NewsletterForm(forms.ModelForm):
    """Formulaire d'inscription à la newsletter"""
    class Meta:
        model = Newsletter
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'input-field',
                    'placeholder': 'Votre nom'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'input-field',
                    'placeholder': 'Votre email'
                }
            )
        }