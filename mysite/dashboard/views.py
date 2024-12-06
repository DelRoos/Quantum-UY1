from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from members.models import Profile
from research.models import ProjetRecherche
from blog.models import Post
from django.views.generic import ListView

User  = get_user_model()

def dashboard(request):
    list_member = Profile.objects.all()
    list_projet = ProjetRecherche.objects.all()
    list_article = Post.objects.all()

    return render(
        request, 
        'modèle/accueil/accueil.html', 
        {
            'list_member': list_member,
            'list_projet': list_projet,
            'list_article': list_article
        }
    )

def member(request, pk):
    member = get_object_or_404(Profile, pk=pk)
    user = get_object_or_404(User, pk=pk) 
    article = Post.objects.filter(author=user, status=Post.Status.PUBLISHED)  
    projets = ProjetRecherche.objects.filter(members=member)

    # article = Post.objects.all()

    return render(
        request, 
        'members/index.html', 
        {
            'member': member,
            'projets': projets,
            'article': article
        }
    )



def recherche_list(request):
    recherche_list = ProjetRecherche.objects.all()
    return render(request, 'modèle/recherches/affichage_sujets.html', {'recherche_list': recherche_list}) 

def vue_projet(request, pk):
    recherche_list = get_object_or_404(ProjetRecherche, pk=pk)
    membres = recherche_list.members.all()
    return render(request, 'modèle/recherches/sujet.html', {'recherche_list': recherche_list, 'membres': membres}) 

def about(request):
    return render(request, 'modèle/about/about.html')

