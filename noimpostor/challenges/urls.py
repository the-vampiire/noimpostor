from django.urls import path, re_path
from .views import create_challenge, view_challenge, edit_challenge

app_name = 'challenges'

urlpatterns = [
    path('create', create_challenge, name = 'create'),
    re_path(r'^(?P<challenge_id>\d+)$', view_challenge, name = 'view'),
    path('<int:challenge_id>/edit', edit_challenge, name = 'edit')
]