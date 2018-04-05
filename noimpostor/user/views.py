from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def profile(request, id):
    context = {
        'user': get_object_or_404(User, pk = id)
    }
    return render(request, 'user/profile.html', context)

