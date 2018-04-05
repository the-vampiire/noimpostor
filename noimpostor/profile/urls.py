from django.urls import path
from .views import profile, update

app_name = 'profile'

urlpatterns = [
    path('', profile, name = 'profile'), # username passed from root.urls
    path('update', update, name = 'update')
]