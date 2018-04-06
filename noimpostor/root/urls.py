from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', include('user_actions.urls', namespace = 'actions'))
    re_path(r'^@(?P<username>\w{4,20})/', include('profile.urls', namespace = 'profile')),
]
