from django import forms
from django.contrib.auth.models import User
from .models import MemberEmail

class MemberEmailForm(forms.ModelForm):
    class Meta:
        model = MemberEmail
        fields = ['email']

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']