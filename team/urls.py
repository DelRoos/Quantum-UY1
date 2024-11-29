from django.urls import path
from .views import TeamListView, TeamMemberDetailView

app_name = 'team'

urlpatterns = [
    path('', TeamListView.as_view(), name='team_list'),
    path('<slug:slug>/', TeamMemberDetailView.as_view(), name='member_detail'),
]
