from django.urls import path
from .import views


app_name = 'dashboard'

urlpatterns = [
    path("" ,views.dashboard),
    path('about/' ,views.about),
    path('<int:pk>/', views.member),
    path('list/', views.recherche_list, name='list'),
    path('list/<int:pk>/', views.vue_projet),
    
]
