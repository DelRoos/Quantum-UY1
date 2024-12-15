from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from members.models import Profile
from research.models import ProjetRecherche
from blog.models import Post


User  = get_user_model()

def dashboard(request):
    list_member = Profile.objects.all()
    list_projet = ProjetRecherche.objects.all()[:5]
    list_article = Post.objects.all()[:3]

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
    article = Post.objects.filter(author=member.user, status=Post.Status.PUBLISHED)  
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


def list_member(request):
    list_member = Profile.objects.all()

    members_by_role = {}
    for member in list_member:
        role_name = member.role
        if role_name not in members_by_role:
            members_by_role[role_name] = []
        members_by_role[role_name].append(member)

    return render(
        request, 
        'members/list.html', 
        {
            'list_member': list_member,
            'members_by_role': members_by_role,

        }
    )
