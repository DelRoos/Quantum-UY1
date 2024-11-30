from django.shortcuts import render, redirect
from .models import ProjetRecherche
from .forms import ProjetRechercheForm

def creer_projet(request):
    if request.method == 'POST':
        form = ProjetRechercheForm(request.POST)
        if form.is_valid():
            projet = form.save()  # Sauvegarde le projet
            # Les membres sont automatiquement associés grâce à la relation ManyToMany
            return redirect('research/research_form.html')  # Remplacez par l'URL de redirection souhaitée
    else:
        form = ProjetRechercheForm()
    return render(request, 'research/research_form.html', {'form': form})


def recherche_list(request):
    recherche_list = ProjetRecherche.objects.all()
    return render(request, 'modèle/accueil/accueil.html', {'recherche_list': recherche_list})