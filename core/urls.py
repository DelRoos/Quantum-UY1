from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
]