from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from .models import SiteConfig
from .forms import ContactForm, NewsletterForm

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter_form'] = NewsletterForm()
        return context
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import SiteConfig

def contact(request):
    # Récupérer la configuration du site
    try:
        site_config = SiteConfig.objects.first()
    except SiteConfig.DoesNotExist:
        site_config = None
    
    # Traitement du formulaire
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Envoyer un email de notification
            # send_mail(
            #     f'Nouveau message de {contact.name}',
            #     contact.message,
            #     settings.DEFAULT_FROM_EMAIL,
            #     [settings.ADMIN_EMAIL],
            #     fail_silently=False,
            # )
            
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    # Préparation du contexte
    context = {
        'form': form,
        'site_config': site_config,
        'page_title': 'Contact',
        'page_description': 'Contactez l\'équipe du laboratoire Quantum UY1',
        'social_links': {
            'twitter': site_config.twitter_url if site_config else '',
            'linkedin': site_config.linkedin_url if site_config else '',
            'researchgate': site_config.researchgate_url if site_config else '',
        } if site_config else {},
        'contact_info': {
            'address': site_config.address if site_config else '',
            'phone': site_config.phone if site_config else '',
            'email': site_config.contact_email if site_config else settings.DEFAULT_FROM_EMAIL,
        }
    }
    
    return render(request, 'core/contact.html', context)

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                f"Merci {form.cleaned_data['name']} ! Vous êtes maintenant inscrit à notre newsletter."
            )
        else:
            if 'email' in form.errors:
                messages.error(
                    request, 
                    "Cette adresse email est déjà inscrite à notre newsletter."
                )
            else:
                messages.error(
                    request, 
                    "Une erreur s'est produite. Veuillez réessayer."
                )
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))