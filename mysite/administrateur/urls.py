from django.urls import path
from . import views


app_name = 'administrateur'


urlpatterns = [
    path('title/', views.creer_titre, name='title'),
    path('epertise/', views.creer_expert, name='epertise'),
]

