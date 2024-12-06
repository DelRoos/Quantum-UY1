from django.shortcuts import get_object_or_404, render, redirect
from .models import ProjetRecherche
from .forms import ProjetRechercheForm

def creer_projet(request):
    if request.method == 'POST':
        form = ProjetRechercheForm(request.POST)
        if form.is_valid():
            projet = form.save() 
            return redirect('modèle/recherches/research_form.html')  
    else:
        form = ProjetRechercheForm()
    return render(request, 'modèle/recherches/research_form.html', {'form': form})



