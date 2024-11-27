from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('<int:pk>/', views.member_detail, name='member_detail'),
    path('create/', views.member_create, name='member_create'),
    path('<int:pk>/update/', views.member_update, name='member_update'),
    path('delete/', views.member_delete, name='member_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)