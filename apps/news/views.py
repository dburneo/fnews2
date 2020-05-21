from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from apps.customuser.forms import SignUpForm, ProfileForm
from social_django.models import UserSocialAuth

from apps.customuser.models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# @login_required
def home(request):
    return render(request, 'news/home.html')

@login_required
def settings(request):
    user = request.user

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'registration/settings.html', {
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm
    
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            # messages.success(request, 'Your password was successfully updated!')
            messages.success(request, 'Tu contraseña se ha cambiado correctamente!')
            return redirect('password')
        else:
            # messages.error(request, 'Please correct the error below.')
            messages.error(request, 'Favor corregir los siguientes errores.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})


@login_required
def profile(request):
    profile = request.user
    if request.method == 'GET':
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            form.save()
            messages.success(request, 'Cambios guardados correctamente!')
        return redirect('profile')
    return render(request, 'registration/profile.html', {'form': form})
