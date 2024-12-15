from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import ProjetRecherche
from .forms import ProjetRechercheForm, CommentForm
from django.views.generic import ListView



def creer_projet(request):
    if request.method == 'POST':
        form = ProjetRechercheForm(request.POST, request.FILES)  
        if form.is_valid():
            projet = form.save()  
            return redirect('research:creer')  
    else:
        form = ProjetRechercheForm()  
    
    return render(request, 'modèle/recherches/research_form.html', {'form': form})


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
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    recherche_list = ProjetRecherche.objects.all()
    return render(request, 'modèle/recherches/affichage_sujets.html', {'recherche_list' : recherche_list, 'posts': posts, 'paginator': paginator}) 



def vue_projet(request, slug):
    recherche_list = get_object_or_404(
        ProjetRecherche,
        slug=slug,
    )
    membres = recherche_list.members.all()

    # FAQ = recherche_list.FAQ.filter(active=True)[:3]

    form = CommentForm(request.POST if request.method == 'POST' else None)

    
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.projet = recherche_list
        comment.save()
        form = CommentForm() 

    context = {
        'recherche_list': recherche_list, 
        'form': form, 
        # 'comment': comment, 
        'membres': membres
    }

    return render(request, 'modèle/recherches/sujet.html', context) 



def about(request):
    return render(request, 'modèle/about/about.html')