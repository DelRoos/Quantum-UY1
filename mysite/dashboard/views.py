from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView
from members.models import Profile, Education
from research.models import ProjetRecherche
from blog.models import Post


User  = get_user_model()

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'modèle/blog/affichage_articles.html'


def dashboard(request):
    list_member = Profile.objects.all()
    list_projet = ProjetRecherche.objects.all()[:5]
    list_article = Post.published.all()[:3]

    return render(
        request, 
        'modèle/accueil/accueil.html', 
        {
            'list_member': list_member,
            'list_projet': list_projet,
            'list_article': list_article
        }
    )

def member(request, slug):
    member = get_object_or_404(Profile, slug=slug)
    user = member.user
    article = Post.objects.filter(author=member.user, status=Post.Status.PUBLISHED)  
    projets = ProjetRecherche.objects.filter(members=member)
    parcours = Education.objects.filter(user=user)


    # article = Post.objects.all()

    return render(
        request, 
        'members/index.html', 
        {
            'member': member,
            'projets': projets,
            'article': article,
            'parcours': parcours
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
