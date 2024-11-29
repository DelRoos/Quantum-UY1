from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Newsletter, Contact

@receiver(post_save, sender=Newsletter)
def send_welcome_email(sender, instance, created, **kwargs):
    """Envoyer un email de bienvenue lors de l'inscription à la newsletter"""
    if created:
        print("Saved user newsletter")
        # send_mail(
        #     'Bienvenue sur la newsletter de Quantum UY1',
        #     'Merci de vous être inscrit à notre newsletter. Vous recevrez nos actualités régulièrement.',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [instance.email],
        #     fail_silently=False,
        # )

@receiver(post_save, sender=Contact)
def notify_new_contact(sender, instance, created, **kwargs):
    """Notifier les administrateurs d'un nouveau message de contact"""
    if created:
        
        print("Saved user contact")
        # send_mail(
        #     f'Nouveau message de contact de {instance.name}',
        #     f'Sujet: {instance.subject}\nMessage: {instance.message}',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [settings.ADMIN_EMAIL],
        #     fail_silently=False,
        # )