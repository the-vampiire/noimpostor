from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, DefaultPrivacyForm
from django.contrib.auth.models import User
from .models import DefaultPrivacy, Follow
from django.db import IntegrityError

def overview(request, username):
    """
    User overview page

    displays user accomplishments, challenges, and conquers [conquered challenges]
    """
    user = get_object_or_404(User, username = username)
    
    context = { 
        'title': "%s%s's Profile" % (user.username[0].upper(), user.username[1:]),
        'user': user,
        # render 'update profile' button if the logged-in user is on their own overview page
        'editable': user == request.user 
    }

    # authed user viewing another users profile page
    if user != request.user:
        # set 'following' boolean if the authed user is following the profile user
        context['following'] = request.user.following.all().filter(following = user).count() == 1

    return render(request, 'profile/overview.html', context)

@login_required(login_url = 'actions:login')
def update(request, username):
    # redirect for tricksy hobbitses that append /update to another users page
    if username != request.user.username:
        return redirect(reverse('profile:overview', kwargs = { 'username': username }))

    update_form = UserUpdateForm(request.POST or None, instance = request.user)
    privacy_form = DefaultPrivacyForm(
        request.POST or None,
        # pre-select users existing setting
        initial = { 'setting': request.user.defaultprivacy.setting }
    )

    if request.method == 'POST' and all((update_form.is_valid(), privacy_form.is_valid())):
        user = update_form.save()
        user.defaultprivacy.setting = privacy_form.cleaned_data['setting']
        user.defaultprivacy.save()

        # TODO: add a flash success message on redirect
        return redirect(reverse('profile:overview', kwargs = { 'username': user.username }))

    # GET
    context = {
            'title': 'Profile Update',
            'update_form': update_form,
            'privacy_form': privacy_form
    }
    return render(request, 'profile/update.html', context)

@login_required(login_url = 'actions:login')
def follow(request, username):
    user = get_object_or_404(User, username = username)
    
    # if a tricksy hobbitses try to follow themself
    if user != request.user:
        try:
            Follow(following = user, follower = request.user).save()
        except IntegrityError as error:
            # user is already following and raises unique constraint ('following', 'follower') error
            # ignore and proceed to redirect
            pass

    return redirect(reverse('profile:overview', kwargs = { 'username': username }))

@login_required(login_url = 'actions:login')
def unfollow(request, username):
    follow = get_object_or_404(
        Follow,
        follower = request.user,
        following = User.objects.get(username = username)
    )

    follow.delete()
    # TODO: add flash success message
    return redirect(reverse('profile:overview', kwargs = { 'username': username }))
