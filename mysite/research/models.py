from django.contrib.auth.models import User
from django.db import models
from members.models import Profile
from autoslug import AutoSlugField



class ProjetRecherche(models.Model): 
    photo = models.ImageField(
        upload_to='research/%Y/%m/%d/',
        blank=True
    ) 
    titre = models.CharField(max_length=200) 
    slug = AutoSlugField(
        populate_from='titre',
    ) 
    problematique = models.TextField()  
    methode_recherche = models.TextField()  
    members = models.ManyToManyField('members.Profile')  
    domaines_application = models.TextField()  
    resultats_impacts = models.TextField()  
    resumé = models.TextField()

class FAQ(models.Model):
    projet = models.ForeignKey(
        ProjetRecherche,
        on_delete=models.CASCADE,
        related_name='FAQ'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    question = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.projet}'