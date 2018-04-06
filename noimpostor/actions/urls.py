from django.urls import re_path, path
from .views import user_login

app_name = 'actions'

urlpatterns = [
    path('login', user_login, name = 'login')
]