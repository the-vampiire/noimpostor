from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, logout
from profile.forms import DefaultPrivacyForm
from django.contrib.auth.models import User
from profile.models import DefaultPrivacy

def user_register(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile:overview', kwargs = { 'username': request.user.username }))

    register_form = UserCreationForm(data = request.POST or None)
    privacy_form = DefaultPrivacyForm(data = request.POST or None)
    
    if request.method == 'POST' and all((register_form.is_valid(), privacy_form.is_valid())):
        user = register_form.save()

        DefaultPrivacy(
            user = user,
            setting = privacy_form.cleaned_data['setting']
        ).save()

        login(request, user)
        return redirect(reverse('profile:overview', kwargs = { 'username': user.username }))
    
    # GET or invalid form -> re-render the form [blank or with errors]
    context = {
        'title': 'Register',
        'register_form': register_form,
        'privacy_form': privacy_form
    }
    return render(request, 'actions/register.html', context)

def user_login(request):
    # redirect an already logged in user
    if request.user.is_authenticated:
        return redirect(reverse('profile:overview', kwargs = { 'username': request.user.username }))
        
    login_form = AuthenticationForm(data = request.POST or None)
    # TODO: cookie setting for where user should redirect on login
    # TODO: add cookie setting option to 'profile:update' view
    next = request.GET.get('next') or request.COOKIES.get('login_redirect')

    # POST for validation + login
    if request.method == 'POST' and login_form.is_valid():
        user = login_form.get_user()
        login(request, user)
        return redirect(next or reverse('profile:overview', kwargs = { 'username': user.username }))
    
    # GET or invalid form -> re-render the form [blank or with errors]
    context = {
        'title': 'Log In',
        'form': login_form,
        'next': next 
    }
    return render(request, 'actions/login.html', context)

@login_required(login_url = 'actions:login')
def user_logout(request):
    logout(request)
    return redirect('/') # return logged out user to home page
