from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm 

from .forms import TitleCreationForm, ExpertiseFieldForm

def creer_titre(request):
    if request.method == 'POST':
        form = TitleCreationForm(request.POST)
        if form.is_valid():
            titre = form.save()  
            # return redirect('title_form.html') 
    else:
        form = TitleCreationForm()
    return render(request, 'admin/title_form.html', {'form': form})

def creer_expert(request):
    if request.method == 'POST':
        form = ExpertiseFieldForm(request.POST)
        if form.is_valid():
            expert = form.save()  
            # return redirect('admin/expert_form.html') 
    else:
        form = ExpertiseFieldForm()
    return render(request, 'admin/expert_form.html', {'form': form})

    