from django import forms
from .models import Comment, Post

class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Votre nom'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Votre email'
        })
    )
    to = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Email du destinataire'
        })
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Vos commentaires',
            'rows': 4
        })
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',  # Utilisez 'form-input' pour correspondre à votre style
                'placeholder': 'Votre nom',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',  # Utilisez 'form-input' pour correspondre à votre style
                'placeholder': 'Votre email',
                'required': 'required'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-textarea',  # Utilisez 'form-textarea' pour correspondre à votre style
                'placeholder': 'Votre commentaire',
                'rows': 4,
                'required': 'required'
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'title', 'body', 'status']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full mb-3'
            }),
            'title': forms.TextInput(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
                'placeholder': 'Titre du post'
            }),
            'body': forms.Textarea(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
                'placeholder': 'Contenu du post',
                'rows': 6
            }),
            'status': forms.Select(attrs={
                'class': 'block w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring focus:ring-purple-500 text-black',
            }),
        }