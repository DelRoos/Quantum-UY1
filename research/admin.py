# research/admin.py
from django.contrib import admin
from .models import (
    ResearchArea,
    Project,
    ProjectImage,
    ProjectDocument,
    ProjectUpdate,
    Collaboration,
    ProjectView
)


@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

class ProjectImageInline(admin.TabularInline):
    model = Project.gallery_images.through  # Utilisez le modèle intermédiaire généré automatiquement
    extra = 1



class ProjectDocumentInline(admin.TabularInline):
    model = Project.documents.through
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'research_area', 'status', 'priority', 'start_date', 'end_date', 
        'is_featured', 'is_public', 'view_count'
    )
    list_filter = ('status', 'priority', 'is_featured', 'is_public', 'research_area')
    search_fields = ('title', 'summary', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline, ProjectDocumentInline]
    autocomplete_fields = ('leader', 'team_members')
    ordering = ('-start_date',)
    exclude = ('gallery_images',)  # Exclure ce champ car il est géré via l'inline



@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    ordering = ('order',)
    search_fields = ('title',)


@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'is_public', 'created_at', 'created_by')
    list_filter = ('document_type', 'is_public')
    search_fields = ('title', 'description')


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'date', 'is_major', 'created_at', 'created_by')
    list_filter = ('is_major', 'project')
    search_fields = ('title', 'content')
    ordering = ('-date',)


@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution_type', 'country', 'is_active', 'start_date', 'end_date')
    list_filter = ('institution_type', 'country', 'is_active')
    search_fields = ('name', 'description', 'summary')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(ProjectView)
class ProjectViewAdmin(admin.ModelAdmin):
    list_display = ('project', 'ip_address', 'user_agent', 'created_at')
    search_fields = ('project__title', 'ip_address', 'user_agent')
    ordering = ('-created_at',)
