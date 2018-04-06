from django.contrib import admin
from django.urls import path, re_path, include
from actions.views import user_login

urlpatterns = [
    path('', user_login), # TODO: add a site app for the index and about views
    path('admin/', admin.site.urls),
    path('actions/', include('actions.urls', namespace = 'actions')),
    re_path(r'^@(?P<username>\w{4,20})/', include('profile.urls', namespace = 'profile')),
]
