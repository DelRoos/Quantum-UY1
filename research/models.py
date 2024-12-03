# research/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from markymark.fields import MarkdownField
from taggit.managers import TaggableManager
from team.models import TeamMember
from dateutil.relativedelta import relativedelta

class ResearchArea(models.Model):
    """Domaines de recherche"""
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField("Description courte", max_length=200)
    description = MarkdownField("Description complète")
    icon = models.ImageField("Icône", upload_to='research/icons/', blank=True)
    banner_image = models.ImageField("Image bannière", upload_to='research/banners/', blank=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    tags = TaggableManager("Mots-clés")
    is_active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Domaine de recherche"
        verbose_name_plural = "Domaines de recherche"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('research:area_detail', kwargs={'slug': self.slug})

class Project(models.Model):
    """Projets de recherche"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('planned', 'Planifié'),
        ('ongoing', 'En cours'),
        ('completed', 'Terminé'),
        ('suspended', 'Suspendu'),
    ]
    
    FUNDING_TYPE_CHOICES = [
        ('internal', 'Financement interne'),
        ('external', 'Financement externe'),
        ('mixed', 'Financement mixte'),
        ('unfunded', 'Sans financement'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Basse'),
        (2, 'Moyenne'),
        (3, 'Haute'),
        (4, 'Critique'),
    ]

    # Informations de base
    title = models.CharField("Titre", max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    research_area = models.ForeignKey(
        ResearchArea, 
        verbose_name="Domaine de recherche",
        on_delete=models.CASCADE, 
        related_name='projects'
    )
    
    # Équipe
    leader = models.ForeignKey(
        TeamMember,
        verbose_name="Responsable",
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_projects'
    )
    team_members = models.ManyToManyField(
        TeamMember,
        verbose_name="Membres de l'équipe",
        related_name='projects'
    )
    
    # Statut et priorité
    status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.IntegerField("Priorité", choices=PRIORITY_CHOICES, default=2)
    
    # Financement
    funding_type = models.CharField(
        "Type de financement",
        max_length=20,
        choices=FUNDING_TYPE_CHOICES,
        default='internal'
    )
    funding_amount = models.DecimalField(
        "Montant du financement",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    funding_details = MarkdownField("Détails du financement", blank=True)
    
    # Dates
    start_date = models.DateField("Date de début")
    end_date = models.DateField("Date de fin", null=True, blank=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)
    
    # Contenu
    summary = MarkdownField("Résumé")
    description = MarkdownField("Description")
    objectives = MarkdownField("Objectifs")
    methodology = MarkdownField("Méthodologie", blank=True)
    expected_results = MarkdownField("Résultats attendus", blank=True)
    current_progress = MarkdownField("Avancement actuel", blank=True)
    challenges = MarkdownField("Défis et obstacles", blank=True)
    
    # Médias et ressources
    image = models.ImageField("Image principale", upload_to='research/projects/', blank=True)
    gallery_images = models.ManyToManyField(
        'ProjectImage',
        verbose_name="Galerie d'images",
        blank=True,
        related_name='projects'
    )
    documents = models.ManyToManyField(
        'ProjectDocument',
        verbose_name="Documents",
        blank=True,
        related_name='projects'
    )
    
    # Métriques et visibilité
    tags = TaggableManager("Mots-clés")
    is_featured = models.BooleanField("Mis en avant", default=False)
    is_public = models.BooleanField("Public", default=True)
    view_count = models.PositiveIntegerField("Nombre de vues", default=0)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('research:research_detail', kwargs={'slug': self.slug})

    @property
    def duration_months(self):
        if not self.end_date:
            return None
        diff = relativedelta(self.end_date, self.start_date)
        return diff.years * 12 + diff.months

    @property
    def completion_percentage(self):
        """Calcule le pourcentage d'avancement basé sur la durée"""
        if not self.end_date or self.status not in ['ongoing', 'completed']:
            return 0
        total_days = (self.end_date - self.start_date).days
        days_passed = (min(self.end_date, timezone.now().date()) - self.start_date).days
        return min(100, int((days_passed / total_days) * 100))

class ProjectImage(models.Model):
    """Images associées aux projets"""
    title = models.CharField("Titre", max_length=200)
    image = models.ImageField("Image", upload_to='research/projects/gallery/')
    caption = models.TextField("Légende", blank=True)
    order = models.PositiveIntegerField("Ordre", default=0)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Image de projet"
        verbose_name_plural = "Images de projets"

    def __str__(self):
        return self.title

class ProjectDocument(models.Model):
    """Documents associés aux projets"""
    DOCUMENT_TYPES = [
        ('report', 'Rapport'),
        ('publication', 'Publication'),
        ('presentation', 'Présentation'),
        ('data', 'Données'),
        ('other', 'Autre'),
    ]

    title = models.CharField("Titre", max_length=200)
    document_type = models.CharField("Type", max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField("Fichier", upload_to='research/projects/documents/')
    description = models.TextField("Description", blank=True)
    is_public = models.BooleanField("Public", default=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    created_by = models.ForeignKey(
        TeamMember,
        verbose_name="Créé par",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Document de projet"
        verbose_name_plural = "Documents de projets"

    def __str__(self):
        return self.title

class ProjectUpdate(models.Model):
    """Mises à jour périodiques des projets"""
    project = models.ForeignKey(
        Project,
        verbose_name="Projet",
        on_delete=models.CASCADE,
        related_name='updates'
    )
    title = models.CharField("Titre", max_length=200)
    content = MarkdownField("Contenu")
    date = models.DateField("Date")
    created_by = models.ForeignKey(
        TeamMember,
        verbose_name="Créé par",
        on_delete=models.SET_NULL,
        null=True
    )
    is_major = models.BooleanField("Mise à jour majeure", default=False)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Mise à jour de projet"
        verbose_name_plural = "Mises à jour de projets"

    def __str__(self):
        return f"{self.project.title} - {self.title}"

class Collaboration(models.Model):
    """Collaborations avec d'autres institutions"""
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField("Logo", upload_to='collaborations/logos/')
    website = models.URLField("Site web")
    institution_type = models.CharField("Type d'institution", max_length=100)
    country = models.CharField("Pays", max_length=100)
    
    description = MarkdownField("Description")
    summary = MarkdownField("Résumé", blank=True)
    projects = models.ManyToManyField(
        Project,
        verbose_name="Projets",
        blank=True,
        related_name='collaborations'
    )
    tags = TaggableManager("Mots-clés")
    
    # Dates et statut
    start_date = models.DateField("Date de début")
    end_date = models.DateField("Date de fin", null=True, blank=True)
    is_active = models.BooleanField("Active", default=True)
    
    # Contact
    contact_name = models.CharField("Nom du contact", max_length=100, blank=True)
    contact_email = models.EmailField("Email du contact", blank=True)
    contact_phone = models.CharField("Téléphone du contact", max_length=20, blank=True)
    
    # Documents
    mou = models.FileField(
        "Protocole d'accord",
        upload_to='collaborations/documents/',
        blank=True,
        help_text="Memorandum of Understanding"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = "Collaboration"
        verbose_name_plural = "Collaborations"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('research:collaboration_detail', kwargs={'slug': self.slug})

class ProjectView(models.Model):
    """Suivi des vues des projets"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_views'
    )
    ip_address = models.GenericIPAddressField("Adresse IP")
    user_agent = models.CharField("User Agent", max_length=200, blank=True)
    created_at = models.DateTimeField("Date de visite", auto_now_add=True)

    class Meta:
        unique_together = ['project', 'ip_address']
        verbose_name = "Vue de projet"
        verbose_name_plural = "Vues de projets"