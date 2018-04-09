from django.urls import path, re_path
from .views import create_accomplishment, view_accomplishment, edit_accomplishment, user_accomplishments, all_accomplishments

app_name = 'accomplishments'

urlpatterns = [
    path('', all_accomplishments, name = 'all'),
    path('create', create_accomplishment, name = 'create'),
    re_path(r'^(?P<accomplishment_id>\d+)$', view_accomplishment, name = 'view'),
    path('<int:accomplishment_id>/edit', edit_accomplishment, name = 'edit'),
    re_path(r'^@(?P<username>\w{4,20})$', user_accomplishments, name = 'user')
]