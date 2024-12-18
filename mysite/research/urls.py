from django.urls import path
from . import views


app_name = 'research'


urlpatterns = [
    
    path('creer/', views.creer_projet, name='creer'),
    path('', views.recherche_list, name='list'),
    path('<slug:slug>/', views.vue_projet, name='detail'),
    
]
