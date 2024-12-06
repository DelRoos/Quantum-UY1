from django.contrib.auth.models import User
from django.db import models
from members.models import Profile



class ProjetRecherche(models.Model): 
    photo = models.ImageField(
        upload_to='research/%Y/%m/%d/',
        blank=True
    ) 
    titre = models.CharField(max_length=200)  
    problematique = models.TextField()  
    methode_recherche = models.TextField()  
    members = models.ManyToManyField('members.Profile')  
    domaines_application = models.TextField()  
    resultats_impacts = models.TextField()  
    resumé = models.TextField()

