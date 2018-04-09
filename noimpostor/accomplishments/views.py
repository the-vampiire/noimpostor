from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Accomplishment, Inspiration
from django.contrib.auth.models import User
from .forms import AccomplishmentForm
from django.db import IntegrityError
from root.base_models import Privacy
from django.http import HttpResponse

def all_accomplishments(request):
    context = {
        'title': 'Public accomplishments',
        'accomplishments': Accomplishment.objects.all().filter(privacy = 1)
    }
    return render(request, 'accomplishments/all.html', context)

def view_accomplishment(request, accomplishment_id):
    """
    renders based on accomplishment privacy setting

    ! authed user may always view their own accomplishments !
    
    private: render private view

    anonymous: display accomplishment data but set 'author' field to 'Anonymous'

    public: display accomplishment data with author username displayed
    """
    accomplishment = get_object_or_404(Accomplishment, id = accomplishment_id)
    privacy = accomplishment.get_privacy_display()

    if privacy == 'private' and request.user != accomplishment.user:
        return render(request, 'global/private.html')
    
    elif request.user == accomplishment.user or privacy == 'public':
        author = accomplishment.user.username
    
    elif privacy == 'anonymous':
        author = 'Anonymous'

    inspiration = request.user.inspirations.all().filter(accomplishment = accomplishment)
    context = {
        'title': "%s's accomplishment" % author,
        'accomplishment': accomplishment,
        'inspiration': inspiration[0].pk if inspiration.count() == 1 else None,
        'author': author
    }
    return render(request, 'accomplishments/view.html', context)

def user_accomplishments(request, username):
    user = get_object_or_404(User, username = username)

    if user.defaultprivacy.get_setting_display() == 'private' and user != request.user:
        return render(request, 'global/private.html')
    
    # display all accomplishments if the authed user is visiting their own page
    if user == request.user:
        accomplishments = user.accomplishments.all()
    # otherwise only display the public accomplishments
    else:
        accomplishments = user.accomplishments.all().filter(privacy = 1)

    context = {
        'title': "%s's Accomplishments" % user.username,
        'accomplishments': accomplishments
    }
    return render(request, 'accomplishments/user.html', context)

@login_required(login_url = 'actions:login')
def create_accomplishment(request):
    form = AccomplishmentForm(
        request.POST or None,
        initial = { 'privacy': request.user.defaultprivacy.setting }
    )
    
    if request.method == 'POST' and form.is_valid():
        new_accomplishment = Accomplishment(user = request.user, **form.cleaned_data)
        new_accomplishment.save()
        return redirect(reverse('accomplishments:view', kwargs = { 'accomplishment_id': new_accomplishment.pk }))
    
    context = {
        'title': 'New Accomplishment',
        'form': form
    }
    return render(request, 'accomplishments/create.html', context)

@login_required(login_url = 'actions:login')
def edit_accomplishment(request, accomplishment_id):
    accomplishment = get_object_or_404(Accomplishment, id = accomplishment_id)
    accomplishment_url = reverse('accomplishments:view', kwargs = { 'accomplishment_id': accomplishment_id })
    # reject the tricksy hobbitses
    if accomplishment.user != request.user:
        return redirect(accomplishment_url)

    form = AccomplishmentForm(
        request.POST or None,
        instance = accomplishment
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(accomplishment_url)

    context = {
        'title': 'Edit Accomplishment',
        'accomplishment_id': accomplishment_id,
        'form': form
    }
    return render(request, 'accomplishments/edit.html', context)

@login_required(login_url = 'actions:login')
def inspiration(request, accomplishment_id):
    accomplishment = get_object_or_404(Accomplishment, id = accomplishment_id)

    if request.method == 'POST' and accomplishment.user != request.user:
        inspiration_id = request.POST.get('inspiration_id')
        
        if inspiration_id == 'None':
            # if no inspiration exists for the user-accomplishment pair
            # create one [in try / except in case a duplicate exists]
            try:
                Inspiration(
                    inspired_user = request.user,
                    accomplishment = accomplishment
                ).save()
            except IntegrityError as error:
                return HttpResponse(status_code = 400, content = error)

        else:
            # inspiration exists for the user-accomplishment pair
            inspiration = get_object_or_404(
                Inspiration,
                inspired_user = request.user,
                accomplishment = Accomplishment.objects.get(id = accomplishment_id)
            )
            # ensure that no tricksy hobbitses have sent an unassociated inspiration id
            if inspiration.id == int(inspiration_id):
                inspiration.delete()

    return redirect(
        reverse('accomplishments:view', kwargs = { 'accomplishment_id': accomplishment_id })
    )

