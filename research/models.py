from django.db import models
from members.models import Member


class ProjetRecherche(models.Model):  
    titre = models.CharField(max_length=200)  
    problematique = models.TextField()  
    methode_recherche = models.TextField()  
    members = models.ManyToManyField('members.Member')  
    domaines_application = models.TextField()  
    resultats_impacts = models.TextField()  
    resumé = models.TextField()  

