# blog/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from markymark.fields import MarkdownField
from taggit.managers import TaggableManager
from team.models import TeamMember

class Category(models.Model):
    """Catégories d'articles"""
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = MarkdownField("Description", blank=True)
    icon = models.ImageField("Icône", upload_to='blog/categories/icons/', blank=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_active = models.BooleanField("Active", default=True)
    parent = models.ForeignKey(
        'self',
        verbose_name="Catégorie parente",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})

class Post(models.Model):
    """Articles du blog"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('review', 'En révision'),
        ('scheduled', 'Programmé'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    ]

    # Informations de base
    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(
        TeamMember,
        verbose_name="Auteur",
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'
    )
    co_authors = models.ManyToManyField(
        TeamMember,
        verbose_name="Co-auteurs",
        related_name='co_authored_posts',
        blank=True
    )

    # Catégorisation
    category = models.ForeignKey(
        Category,
        verbose_name="Catégorie",
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    tags = TaggableManager("Mots-clés")

    # Contenu
    excerpt = MarkdownField("Extrait", help_text="Bref résumé de l'article")
    content = MarkdownField("Contenu")
    featured_image = models.ImageField(
        "Image à la une",
        upload_to='blog/featured_images/',
        blank=True
    )
    banner_image = models.ImageField(
        "Image bannière",
        upload_to='blog/banner_images/',
        blank=True
    )

    # Statut et visibilité
    status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField("Mis en avant", default=False)
    allow_comments = models.BooleanField("Autoriser les commentaires", default=True)
    is_premium = models.BooleanField("Contenu premium", default=False)

    # Dates
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)
    published_at = models.DateTimeField("Publié le", null=True, blank=True)
    scheduled_for = models.DateTimeField("Programmé pour", null=True, blank=True)

    # SEO
    meta_description = models.CharField("Meta description", max_length=160, blank=True)
    meta_keywords = models.CharField("Meta mots-clés", max_length=200, blank=True)

    # Statistiques
    view_count = models.PositiveIntegerField("Nombre de vues", default=0)
    read_time = models.PositiveIntegerField(
        "Temps de lecture",
        default=0,
        help_text="Temps de lecture estimé en minutes"
    )

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        indexes = [
            models.Index(fields=['-published_at', '-created_at']),
            models.Index(fields=['status', 'published_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Calcul automatique du temps de lecture
        word_count = len(self.content.split())
        self.read_time = max(1, round(word_count / 200))
        
        # Gestion de la date de publication
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        """Vérifie si l'article est publié"""
        return (
            self.status == 'published' and 
            self.published_at and 
            self.published_at <= timezone.now()
        )

    @property
    def related_posts(self):
        """Retourne les articles connexes basés sur la catégorie et les tags"""
        return Post.objects.published().filter(
            models.Q(category=self.category) |
            models.Q(tags__in=self.tags.all())
        ).exclude(id=self.id).distinct()[:3]

    @classmethod
    def published(cls):
        """Gestionnaire personnalisé pour les articles publiés"""
        return cls.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        )

class PostImage(models.Model):
    """Images dans le contenu des articles"""
    post = models.ForeignKey(
        Post,
        verbose_name="Article",
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField("Image", upload_to='blog/content_images/')
    caption = models.CharField("Légende", max_length=200, blank=True)
    alt_text = models.CharField("Texte alternatif", max_length=200, blank=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Image d'article"
        verbose_name_plural = "Images d'articles"

    def __str__(self):
        return f"Image pour {self.post.title}"

class Comment(models.Model):
    """Commentaires sur les articles"""
    post = models.ForeignKey(
        Post,
        verbose_name="Article",
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        verbose_name="Commentaire parent",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    author = models.ForeignKey(
        TeamMember,
        verbose_name="Auteur",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email")
    website = models.URLField("Site web", blank=True)
    content = MarkdownField("Contenu")
    
    is_approved = models.BooleanField("Approuvé", default=False)
    is_spam = models.BooleanField("Spam", default=False)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    ip_address = models.GenericIPAddressField("Adresse IP", null=True, blank=True)
    user_agent = models.CharField("User Agent", max_length=200, blank=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"

    def __str__(self):
        return f"Commentaire de {self.name} sur {self.post.title}"

    @property
    def is_reply(self):
        """Vérifie si le commentaire est une réponse"""
        return self.parent is not None

class PostView(models.Model):
    """Suivi des vues des articles"""
    post = models.ForeignKey(
        Post,
        verbose_name="Article",
        on_delete=models.CASCADE,
        related_name='post_views'
    )
    ip_address = models.GenericIPAddressField("Adresse IP")
    user_agent = models.CharField("User Agent", max_length=200, blank=True)
    referrer = models.URLField("Référent", blank=True)
    created_at = models.DateTimeField("Date de visite", auto_now_add=True)

    class Meta:
        unique_together = ['post', 'ip_address']
        verbose_name = "Vue d'article"
        verbose_name_plural = "Vues d'articles"

class Tag(models.Model):
    """Tags personnalisés pour les articles"""
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField("Description", blank=True)
    icon = models.ImageField("Icône", upload_to='blog/tags/icons/', blank=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})