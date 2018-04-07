from django.urls import path
from .views import overview, update, follow, unfollow

app_name = 'profile'

# username passed from root.urls
urlpatterns = [ 
    path('', overview, name = 'overview'),
    path('update', update, name = 'update'),
    path('follow', follow, name = 'follow'),
    path('unfollow', unfollow, name = 'unfollow')
]