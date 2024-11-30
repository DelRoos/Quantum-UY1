from django.urls import path
from .views import creer_projet

urlpatterns = [
    path('creer/', creer_projet, name='creer_projet'),
]