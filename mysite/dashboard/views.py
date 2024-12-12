from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from members.models import Profile
from research.models import ProjetRecherche
from blog.models import Post
from django.views.generic import ListView

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


class ProjetRechercheListView(ListView):
    """
    Alternative post list view
    """
    queryset = ProjetRecherche.objects.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'modèle/blog/affichage_sujets.html'


def recherche_list(request):
    posts = ProjetRecherche.objects.all()
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    recherche_list = ProjetRecherche.objects.all()
    return render(request, 'modèle/recherches/affichage_sujets.html', {'recherche_list' : recherche_list, 'posts': posts, 'paginator': paginator}) 

def vue_projet(request, pk):
    recherche_list = get_object_or_404(ProjetRecherche, pk=pk)
    membres = recherche_list.members.all()
    return render(request, 'modèle/recherches/sujet.html', {'recherche_list': recherche_list, 'membres': membres}) 

def about(request):
    return render(request, 'modèle/about/about.html')

