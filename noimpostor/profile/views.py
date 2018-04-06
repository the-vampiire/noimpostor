from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import UserUpdateForm, DefaultPrivacyForm
from django.contrib.auth.models import User
from .models import DefaultPrivacy

from django.http import HttpResponse # TODO: remove when view is completed


def overview(request, username): # username
    user = get_object_or_404(User, username = username)
    return render(
        request,
        'profile/overview.html',
        context = { 
            'user': user,
            'title': "%s%s's Profile" % (user.username[0].upper(), user.username[1:]) 
        }
    )

def update(request, username):
    if not request.user.is_authenticated:
        # TODO: add proper login redirect when user_actions app is complete
        return HttpResponse('Login redirect here')

    update_form = UserUpdateForm(request.POST or None, instance = request.user)
    privacy_form = DefaultPrivacyForm(request.POST or None)

    if request.method == 'POST':
        if update_form.is_valid() and privacy_form.is_valid():
            user = update_form.save()
            user.defaultprivacy.setting = privacy_form.cleaned_data['setting']
            user.defaultprivacy.save()

            # TODO: add a confirmation -> redirect or flash message on redirect
            return redirect(
                reverse(
                    'profile:overview',
                    kwargs = { 'username': user.username }
                )
            )
    # GET
    return render(
        request,
        'profile/update.html',
        context = {
            'update_form': update_form,
            'privacy_form': privacy_form
        }
    )
