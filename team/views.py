from django.views.generic import TemplateView, DetailView
from .models import TeamMember, Position

class TeamListView(TemplateView):
    template_name = 'member_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Grouper les membres par catégorie de position
        context['categories'] = Position.objects.values_list('category', flat=True).distinct()
        context['team_members'] = TeamMember.objects.filter(is_active=True).select_related('position', 'department')
        context['positions'] = Position.objects.all()
        return context


class TeamMemberDetailView(DetailView):
    model = TeamMember
    template_name = 'member_detail.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter des données supplémentaires liées au membre
        context['publications'] = self.object.publications.all()  # Récupérer les publications associées
        context['experiences'] = self.object.experiences.all()  # Récupérer les expériences professionnelles
        context['education_history'] = self.object.education_history.all()  # Récupérer l'historique académique
        context['similar_profiles'] = TeamMember.objects.filter(
            department=self.object.department
        ).exclude(id=self.object.id)[:4]
        return context