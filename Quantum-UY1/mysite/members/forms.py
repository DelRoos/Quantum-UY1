from django import forms
from django.contrib.auth import get_user_model
from .models import Profile, Title, ExpertiseField, Newsletter


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileEditForm(forms.ModelForm):
    expertise = forms.ModelMultipleChoiceField(
        queryset=ExpertiseField.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),  
        required=True
    )
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo', 'title']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full mb-3'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'  # Ajout du type date pour activer le sélecteur
            }),
            'title': forms.Select(attrs={'class': 'form-control'}),
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