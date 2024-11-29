# team/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from markymark.fields import MarkdownField
from taggit.managers import TaggableManager

class Department(models.Model):
    """Départements ou unités de recherche"""
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = MarkdownField("Description")
    head = models.ForeignKey(
        'TeamMember',
        verbose_name="Responsable",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_department'
    )
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Département"
        verbose_name_plural = "Départements"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Position(models.Model):
    """Positions et rôles dans l'équipe"""
    name = models.CharField("Titre", max_length=100)
    category = models.CharField(
        "Catégorie",
        max_length=50,
        choices=[
            ('academic', 'Académique'),
            ('research', 'Recherche'),
            ('administrative', 'Administratif'),
            ('technical', 'Technique'),
            ('student', 'Étudiant'),
        ]
    )
    level = models.PositiveIntegerField("Niveau hiérarchique", default=0)
    description = models.TextField("Description", blank=True)

    class Meta:
        ordering = ['level', 'name']
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    """Membres de l'équipe"""
    # Informations personnelles
    title = models.CharField("Titre", max_length=10, blank=True)  # Dr., Prof., etc.
    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    
    # Position et département
    position = models.ForeignKey(
        Position,
        verbose_name="Position",
        on_delete=models.SET_NULL,
        null=True
    )
    department = models.ForeignKey(
        Department,
        verbose_name="Département",
        on_delete=models.SET_NULL,
        null=True,
        related_name='members'
    )
    
    # Profil détaillé
    photo = models.ImageField("Photo", upload_to='team/photos/', blank=True)
    bio_short = MarkdownField("Biographie courte", help_text="Bref résumé (max 200 mots)")
    bio = MarkdownField("Biographie", blank=True)
    research_interests = MarkdownField("Intérêts de recherche", blank=True)
    expertise = MarkdownField("Expertise", blank=True)
    education = MarkdownField("Formation", blank=True)
    
    # Tags et spécialités
    tags = TaggableManager("Mots-clés")
    specialties = models.ManyToManyField(
        'Specialty',
        verbose_name="Spécialités",
        blank=True
    )
    
    # Liens externes
    website = models.URLField("Site web personnel", blank=True)
    google_scholar = models.URLField("Google Scholar", blank=True)
    researchgate = models.URLField("ResearchGate", blank=True)
    orcid = models.CharField("ORCID", max_length=20, blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    twitter = models.URLField("Twitter", blank=True)
    
    # Statut et ordre
    is_active = models.BooleanField("Actif", default=True)
    is_featured = models.BooleanField("Mis en avant", default=False)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    
    # Dates
    joined_date = models.DateField("Date d'arrivée")
    left_date = models.DateField("Date de départ", null=True, blank=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        ordering = ['order', 'last_name', 'first_name']
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('team:member_detail', kwargs={'slug': self.slug})

class Specialty(models.Model):
    """Spécialités et domaines d'expertise"""
    name = models.CharField("Nom", max_length=100)
    description = models.TextField("Description", blank=True)
    icon = models.ImageField("Icône", upload_to='team/specialties/', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"

    def __str__(self):
        return self.name

class Publication(models.Model):
    """Publications scientifiques"""
    title = models.CharField("Titre", max_length=300)
    authors = models.ManyToManyField(
        TeamMember,
        verbose_name="Auteurs",
        related_name='publications'
    )
    abstract = MarkdownField("Résumé", blank=True)
    journal = models.CharField("Journal", max_length=200, blank=True)
    volume = models.CharField("Volume", max_length=50, blank=True)
    issue = models.CharField("Numéro", max_length=50, blank=True)
    pages = models.CharField("Pages", max_length=50, blank=True)
    doi = models.CharField("DOI", max_length=100, blank=True)
    publication_date = models.DateField("Date de publication")
    
    # Type et catégorie
    PUBLICATION_TYPES = [
        ('article', 'Article de journal'),
        ('conference', 'Article de conférence'),
        ('book', 'Livre'),
        ('book_chapter', 'Chapitre de livre'),
        ('thesis', 'Thèse'),
        ('patent', 'Brevet'),
        ('preprint', 'Preprint'),
    ]
    publication_type = models.CharField(
        "Type de publication",
        max_length=20,
        choices=PUBLICATION_TYPES
    )
    
    # Tags et métriques
    tags = TaggableManager()
    citation_count = models.PositiveIntegerField("Nombre de citations", default=0)
    
    # Fichiers et liens
    pdf = models.FileField("PDF", upload_to='publications/pdfs/', blank=True)
    url = models.URLField("URL", blank=True)
    
    class Meta:
        ordering = ['-publication_date']
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def __str__(self):
        return self.title

class Award(models.Model):
    """Prix et distinctions"""
    name = models.CharField("Nom", max_length=200)
    recipient = models.ForeignKey(
        TeamMember,
        verbose_name="Récipiendaire",
        on_delete=models.CASCADE,
        related_name='awards'
    )
    description = MarkdownField("Description")
    awarding_body = models.CharField("Institution", max_length=200)
    date_received = models.DateField("Date de réception")
    
    class Meta:
        ordering = ['-date_received']
        verbose_name = "Prix"
        verbose_name_plural = "Prix"

    def __str__(self):
        return f"{self.name} - {self.recipient}"

class Education(models.Model):
    """Parcours académique des membres"""
    member = models.ForeignKey(
        TeamMember,
        verbose_name="Membre",
        on_delete=models.CASCADE,
        related_name='education_history'
    )
    degree = models.CharField("Diplôme", max_length=200)
    institution = models.CharField("Institution", max_length=200)
    field_of_study = models.CharField("Domaine d'étude", max_length=200)
    start_date = models.DateField("Date de début")
    end_date = models.DateField("Date de fin", null=True, blank=True)
    description = MarkdownField("Description", blank=True)
    
    class Meta:
        ordering = ['-end_date', '-start_date']
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

    def __str__(self):
        return f"{self.degree} - {self.institution}"

class Experience(models.Model):
    """Expériences professionnelles des membres"""
    member = models.ForeignKey(
        TeamMember,
        verbose_name="Membre",
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    position = models.CharField("Poste", max_length=200)
    company = models.CharField("Organisation", max_length=200)
    location = models.CharField("Lieu", max_length=200)
    start_date = models.DateField("Date de début")
    end_date = models.DateField("Date de fin", null=True, blank=True)
    description = MarkdownField("Description", blank=True)
    is_current = models.BooleanField("Poste actuel", default=False)
    
    class Meta:
        ordering = ['-end_date', '-start_date']
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"

    def __str__(self):
        return f"{self.position} - {self.company}"