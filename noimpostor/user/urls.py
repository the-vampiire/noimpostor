from django.urls import path
from .views import profile

app_name = 'user'

urlpatterns = [
    path('<int:id>', profile, name = 'profile')
]