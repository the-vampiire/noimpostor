from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, logout

def user_login(request):
    # redirect an already logged in user
    if request.user.is_authenticated:
        return redirect(reverse('profile:overview', kwargs = { 'username': request.user.username }))

    # if user is not logged in go into GET/POST form routine
    login_form = AuthenticationForm(data = request.POST or None)

    # POST for validation + login
    if request.method == 'POST' and login_form.is_valid():
        user = login_form.get_user()
        login(request, user)
        return redirect(reverse('profile:overview', kwargs = { 'username': user.username }))
    
    # GET or invalid form -> re-render the form [blank or with errors]
    return render(request, 'actions/login.html', context = { 'form': login_form })

