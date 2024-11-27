from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'title', 'expertise', 'email', 
        'password', 
        'profile_picture']
        widgets = {
            'password': forms.PasswordInput(),
            'expertise': forms.CheckboxSelectMultiple(),  
        }