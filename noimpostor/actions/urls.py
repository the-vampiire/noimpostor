from django.urls import re_path, path
from .views import user_login, user_logout

app_name = 'actions'

urlpatterns = [
    path('login', user_login, name = 'login'),
    path('logout', user_logout, name = 'logout')
]