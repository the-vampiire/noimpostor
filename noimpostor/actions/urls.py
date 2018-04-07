from django.urls import re_path, path
from .views import user_register, user_login, user_logout, follow_user

app_name = 'actions'

urlpatterns = [
    path('register', user_register, name = 'register'),
    path('login', user_login, name = 'login'),
    path('logout', user_logout, name = 'logout'),
    # TODO: uncomment when followers app is completed
    # re_path(r'^follow/(P?<username>\w{4,20})', follow_user, name = 'follow') 
]