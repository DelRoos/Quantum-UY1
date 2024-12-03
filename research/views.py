from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import ResearchArea, Project, Collaboration
from team.models import TeamMember


def research_detail(request, slug):
    # Récupérer le projet en fonction du slug
    project = get_object_or_404(Project, slug=slug, is_public=True)

    # Préparer les données pour l'équipe et les publications
    team_members = project.team_members.all()
    publications = project.leader.publications.all() if project.leader else []

    context = {
        "project": project,
        "team_members": team_members,
        "publications": publications,
    }
    return render(request, 'research_detail.html', context)


def research_home(request):
    # Récupérer les métriques de recherche
    metrics = {
        'research_areas_count': ResearchArea.objects.filter(is_active=True).count(),
        'active_projects_count': Project.objects.filter(status='ongoing', is_public=True).count(),
        'publications_count': 25,  # Exemple statique
        'collaborations_count': Collaboration.objects.filter(is_active=True).count(),
    }

    # Projets vedettes
    featured_projects = Project.objects.filter(is_featured=True, is_public=True).order_by('-start_date')[:2]

    # Pagination pour les projets secondaires
    secondary_projects_list = Project.objects.filter(is_featured=False, is_public=True).order_by('-start_date')
    paginator = Paginator(secondary_projects_list, 6)  # 6 projets par page
    page_number = request.GET.get('page')
    secondary_projects = paginator.get_page(page_number)

    # Collaborations
    collaborations = Collaboration.objects.filter(is_active=True)[:4]

    context = {
        'metrics': metrics,
        'featured_projects': featured_projects,
        'secondary_projects': secondary_projects,
        'collaborations': collaborations,
    }
    
    return render(request, 'research_list.html', context)
