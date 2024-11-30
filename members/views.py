from django.shortcuts import render, get_object_or_404, redirect
from .models import Member
from .forms import MemberForm

# Liste des membres
def member_list(request):
    members = Member.objects.all()
    return render(request, 'modèle/accueil/accueil.html', {'members': members})

# Détails d'un membre
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'members/index.html', {'member': member})

# Ajouter un nouveau membre
def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('members/member_list')
    else:
        form = MemberForm()
    return render(request, 'members/member_form.html', {'form': form})

# Modifier un membre
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_detail', pk=pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/member_form.html', {'form': form})

# Supprimer un membre
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'members/member_confirm_delete.html', {'member': member})
