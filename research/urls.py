from django.urls import path
from .views import research_home, research_detail

app_name = 'research'

urlpatterns = [
    # Page principale avec métriques, projets et collaborations
    path('research_list', research_home, name='research_list'),

    # Détail d'un projet spécifique
    path('<slug:slug>/', research_detail, name='research_detail'),
]
