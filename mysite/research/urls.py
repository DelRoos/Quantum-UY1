from django.urls import path
from . import views


app_name = 'research'


urlpatterns = [
    
    path('creer/', views.creer_projet, name='creer'),
    
]