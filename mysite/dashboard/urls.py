from django.urls import path
from .import views


app_name = 'dashboard'

urlpatterns = [
    path("" ,views.dashboard, name='acceuil'),
    # path('about/' ,views.about),
    path('<int:pk>/', views.member, name='membre'),
    path('list', views.list_member, name='membre_list'),
    
    
]
