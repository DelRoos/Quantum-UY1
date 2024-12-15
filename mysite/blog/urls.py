from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),  
    path('<slug:slug>/', views.post_detail, name='post_detail'),  
    path('create/', views.create_post, name='create_post'), 
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),  
]
