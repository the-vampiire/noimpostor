from django.urls import path, re_path
from .views import (
    create_accomplishment,
    user_accomplishments,
    view_accomplishment,
    edit_accomplishment,
    all_accomplishments,
    inspiration
)

app_name = 'accomplishments'

urlpatterns = [
    re_path(r'^(?P<accomplishment_id>\d+)$', view_accomplishment, name = 'view'),
    re_path(r'^@(?P<username>\w{4,20})$', user_accomplishments, name = 'user'),
    path('<int:accomplishment_id>/edit', edit_accomplishment, name = 'edit'),
    path('<int:accomplishment_id>/inspiration', inspiration, name = 'inspiration'),
    path('create', create_accomplishment, name = 'create'),
    re_path(r'$^', all_accomplishments, name = 'all'),
]