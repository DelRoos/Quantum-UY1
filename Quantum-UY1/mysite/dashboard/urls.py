from django.urls import path
from .import views


app_name = 'dashboard'

urlpatterns = [
    path("" ,views.dashboard, name='acceuil'),
    # path('about/' ,views.about),
    path('members/<slug:slug>/', views.member, name='membre'),
    path('members', views.list_member, name='membre_list'),
        
]
