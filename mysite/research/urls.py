from django.urls import path
from . import views


app_name = 'research'


urlpatterns = [
    
    path('creer/', views.creer_projet, name='creer'),
    path('list/', views.recherche_list, name='list'),
    path('list/<slug:slug>/', views.vue_projet, name='detail'),
    
]
