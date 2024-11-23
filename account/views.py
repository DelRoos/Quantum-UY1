from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import MemberEmail
from .forms import MemberEmailForm, UserCreationForm

def register_email(request):
    if request.method == 'POST':
        form = MemberEmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = MemberEmailForm()
    return render(request, 'accounts/register_email.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # handle invalid login
            pass
    return render(request, 'accounts/login.html')

def request_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            member_email = MemberEmail.objects.get(email=email)
            if User.objects.filter(email=email).exists():
                # Email already has an account
                return render(request, 'accounts/request_account.html', {'error': 'Cet email a déjà un compte.'})
            else:
                return redirect('create_account', email=email)
        except MemberEmail.DoesNotExist:
            return render(request, 'accounts/request_account.html', {'error': 'Email non enregistré.'})
    return render(request, 'accounts/request_account.html')

def create_account(request, email):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/create_account.html', {'form': form, 'email': email})