from django.urls import path
from .views import register_email, login_view, request_account, create_account

urlpatterns = [
    path('register_email/', register_email, name='register_email'),
    path('login/', login_view, name='login'),
    path('request_account/', request_account, name='request_account'),
    path('create_account/<str:email>/', create_account, name='create_account'),
]