from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from root.base_models import Privacy
from .forms import ChallengeForm
from .models import Challenge

def all_challenges(request):
    context = {
        'title': 'Public Challenges',
        'challenges': Challenge.objects.all().filter(privacy = 1)
    }
    return render(request, 'challenges/all.html', context)

def view_challenge(request, challenge_id):
    """
    renders based on Challenge privacy setting

    ! authed user may always view their own Challenges !
    
    private: render private view

    anonymous: display Challenge data but set 'author' field to 'Anonymous'

    public: display Challenge data with author username displayed
    """
    challenge = get_object_or_404(Challenge, id = challenge_id)
    privacy = challenge.get_privacy_display()

    if privacy == 'private' and request.user != challenge.user:
        return render(request, 'global/private.html')
    
    elif request.user == challenge.user or privacy == 'public':
        author = challenge.user.username
    
    elif privacy == 'anonymous':
        author = 'Anonymous'
            
    context = {
        'title': "%s's Challenge" % author,
        'challenge': challenge,
        'author': author
    }
    return render(request, 'challenges/view.html', context)

def user_challenges(request, username):
    user = get_object_or_404(User, username = username)

    if user.defaultprivacy.get_setting_display() == 'private' and user != request.user:
        return render(request, 'global/private.html')
    
    # display all challenges if the authed user is visiting their own page
    if user == request.user:
        challenges = user.challenges.all()
    # otherwise only display the public challenges
    else:
        challenges = user.challenges.all().filter(privacy = 1)

    context = {
        'title': "%s's Challenges" % user.username,
        'challenges': challenges
    }
    return render(request, 'challenges/user.html', context)

@login_required(login_url = 'actions:login')
def create_challenge(request):
    form = ChallengeForm(
        request.POST or None,
        initial = { 'privacy': request.user.defaultprivacy.setting }
    )
    
    if request.method == 'POST' and form.is_valid():
        new_challenge = Challenge(user = request.user, **form.cleaned_data)
        new_challenge.save()
        return redirect(reverse('challenges:view', kwargs = { 'challenge_id': new_challenge.pk }))
    
    context = {
        'title': 'New Challenge',
        'form': form
    }
    return render(request, 'challenges/create.html', context)

@login_required(login_url = 'actions:login')
def edit_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id = challenge_id)
    challenge_url = reverse('challenges:view', kwargs = { 'challenge_id': challenge_id })
    # reject the tricksy hobbitses
    if challenge.user != request.user:
        return redirect(challenge_url)

    form = ChallengeForm(
        request.POST or None,
        instance = challenge
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(challenge_url)

    context = {
        'title': 'Edit Challenge',
        'challenge_id': challenge_id,
        'form': form
    }
    return render(request, 'challenges/edit.html', context)
