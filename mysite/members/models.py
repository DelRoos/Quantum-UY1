from django.db import models
from django.conf import settings
from django.utils.text import slugify
from autoslug import AutoSlugField



class Title(models.Model):
    TITLE_CHOICES = [
        ('monsieur', 'Mr'),
        ('madame', 'Mme'),
        ('mademoiselle', 'Mll'),
        ('docteur', 'Dr'),
        ('professeur', 'Pr'),
    ]


    name = models.CharField(
        max_length=100,
        choices=TITLE_CHOICES,
        default='monsieur'  
    )
    

    def __str__(self):
        return self.get_name_display() 
    
    class Meta:
        ordering = ['name']  # Tri par ordre alphabétique


        

class Role(models.Model):
    ROLE_CHOICES = [
        ('etudiant_chercheur', 'Étudiant chercheur'),
        ('chercheur', 'Chercheur'),
        ('administrateur', 'Administrateur'),
        ('consultant', 'Consultant'),
        ('scientifique', 'Scientifique'),
    ]

    name = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default='etudiant_chercheur'  # Optionnel : définir une valeur par défaut
    )

    def __str__(self):
        return self.get_name_display() 

    class Meta:
        ordering = ['name']  # Tri par ordre alphabétique



class ExpertiseField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


        
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,

    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,

    )
    slug = AutoSlugField(max_length=255, unique=True, blank=True)
    profession = models.TextField(max_length=150)
    biographie = models.TextField(max_length=150)
    expertise = models.ManyToManyField(ExpertiseField)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True
    )
    website = models.URLField(max_length=100)
    google_scholar = models.URLField(max_length=100)
    researchgate = models.URLField(max_length=100)
    orcid = models.CharField(max_length=100)
    linkedin = models.URLField(max_length=100)
    twitter = models.URLField(max_length=100)

    def __str__(self):
        return f'Profile of {self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.first_name} {self.user.last_name}")
        super().save(*args, **kwargs)


class Education(models.Model):
    """Parcours académique des membres"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    diplome = models.CharField("Diplôme", max_length=200)
    institution = models.CharField("Institution", max_length=200)
    filiere = models.CharField("Domaine d'étude", max_length=200)
    start_date = models.DateField("Date de début")
    end_date = models.DateField("Date de fin", null=True, blank=True)
    
    class Meta:
        ordering = ['-end_date', '-start_date']
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

    def __str__(self):
        return f"{self.diplome} - {self.institution}"




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