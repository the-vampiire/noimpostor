from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def profile(request, username):
    user = get_object_or_404(User, username = username)
    return render(
        request,
        'user/profile.html',
        context = { 
            'user': user,
            'title': "%s%s's Profile" % (user.username[0].upper(), user.username[1:]) 
        }
    )

