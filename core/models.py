from django.db import models

class SiteConfig(models.Model):
    """Configuration globale du site"""
    site_name = models.CharField(max_length=100, default="Quantum UY1")
    site_description = models.TextField(default="Laboratoire de Recherche en Physique Quantique")
    contact_email = models.EmailField(default="contact@quantum-uy1.com")
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Réseaux sociaux
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    researchgate_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configuration du site"
        
class Newsletter(models.Model):
    """Abonnés à la newsletter"""
    name = models.CharField(max_length=100, verbose_name="Nom", null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.name} - {self.email}"

class Contact(models.Model):
    """Messages de contact"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.name} - {self.subject}"