from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm 
from django.http import JsonResponse
from .forms import (
    LoginForm, 
    UserRegistrationForm, 
    UserEditForm,
    ProfileEditForm,
    NewsletterForm
) 
from .models import Profile, Title, Role, Newsletter


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('members:dashboard', user_id=new_user.id)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'modèle/account/register.html', {'user_form': user_form})

    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect('members:dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'modèle/registration/login.html', {'form': form})


@login_required
def create_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile  # Le profil devrait exister à ce stade
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)
    except Profile.DoesNotExist:
        return HttpResponse("Profile not found", status=404)

    if request.method == 'POST':
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('members:dashboard')
    else:
        profile_form = ProfileEditForm(instance=profile)

    return render(
        request,
        'modèle/account/create_profile.html',
        {'profile_form': profile_form}
    )



@login_required
def edit(request):
    # Assurez-vous que l'utilisateur a un profil
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'title': Title.objects.get(id=1),  
            'role': Role.objects.get(id=1)
        }
    )

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('members:dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(
        request,
        'modèle/account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        default_title = Title.objects.get(id=1)
        default_role = Role.objects.get(id=1)  # Remplacez 1 par un ID valide
        Profile.objects.create(user=instance, title=default_role)



@login_required
def dashboard(request):
    return render(
        request,
        'modèle/account/dashboard.html',
        {'section': 'dashboard'}
    )


def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"Merci {form.cleaned_data['name']} ! Vous êtes maintenant inscrit à notre newsletter."
                })
            else:
                messages.success(
                    request, 
                    f"Merci {form.cleaned_data['name']} ! Vous êtes maintenant inscrit à notre newsletter."
                )
        else:
            error_message = "Cette adresse email est déjà inscrite à notre newsletter." if 'email' in form.errors else "Une erreur s'est produite. Veuillez réessayer."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_message,
                    'errors': form.errors
                })
            else:
                messages.error(request, error_message)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'message': "Méthode non autorisée"
        })
    return redirect(request.META.get('HTTP_REFERER', 'base.html'))