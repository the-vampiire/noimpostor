from django.urls import re_path, path
from .views import *

urlpatterns = [
    re_path('', login, name = 'login'),
    
]