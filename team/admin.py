from django.contrib import admin
from .models import Department, Position, TeamMember, Specialty, Publication, Award, Education, Experience

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'order')
    list_filter = ('head',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('level', 'name')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'department', 'is_active', 'is_featured', 'order')
    list_filter = ('is_active', 'is_featured', 'department', 'position')
    search_fields = ('first_name', 'last_name', 'email', 'bio_short', 'bio', 'research_interests')
    autocomplete_fields = ('position', 'department', 'specialties')
    ordering = ('order', 'last_name', 'first_name')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal', 'publication_type', 'publication_date', 'citation_count')
    list_filter = ('publication_type', 'publication_date')
    search_fields = ('title', 'abstract', 'doi', 'journal')
    autocomplete_fields = ('authors',)
    ordering = ('-publication_date',)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipient', 'awarding_body', 'date_received')
    list_filter = ('awarding_body', 'date_received')
    search_fields = ('name', 'description', 'recipient__first_name', 'recipient__last_name', 'awarding_body')
    autocomplete_fields = ('recipient',)
    ordering = ('-date_received',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'field_of_study', 'member', 'start_date', 'end_date')
    list_filter = ('institution', 'field_of_study')
    search_fields = ('degree', 'institution', 'field_of_study', 'description', 'member__first_name', 'member__last_name')
    autocomplete_fields = ('member',)
    ordering = ('-end_date', '-start_date')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'location', 'member', 'start_date', 'end_date', 'is_current')
    list_filter = ('company', 'location', 'is_current')
    search_fields = ('position', 'company', 'location', 'description', 'member__first_name', 'member__last_name')
    autocomplete_fields = ('member',)
    ordering = ('-end_date', '-start_date')
