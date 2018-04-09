from django.urls import path, re_path
from .views import create_challenge, view_challenge

app_name = 'challenges'

urlpatterns = [
    path('create', create_challenge, name = 'create'),
    path('view/<int:challenge_id>', view_challenge, name = 'view'),
    
]