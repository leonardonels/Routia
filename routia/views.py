from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, logout as django_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import ChangeUsernameForm, DeleteProfileForm


def home(request):
    return render(request, 'home.html', {})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/maps/planner/')  # Redirect to planner page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to planner page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    django_logout(request)
    return redirect('home')

def profile_view(request):
    return render(request, 'profile.html')

@login_required
def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.user, request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            request.user.username = new_username
            request.user.save()
            update_session_auth_hash(request, request.user)  # Update session to prevent logout
            messages.success(request, 'Your username has been successfully changed.')
            return redirect('profile')  # Assumi che esista una vista 'profile'
    else:
        form = ChangeUsernameForm(request.user)

    return render(request, 'change_username.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update session to prevent logout
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('profile')  # Assumi che esista una vista 'profile'
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        form = DeleteProfileForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            user.delete()
            messages.success(request, 'Your profile has been successfully deleted.')
            logout(request)  # Logout the user after deleting the profile
            return redirect('home')  # Assumi che esista una vista 'home'
    else:
        form = DeleteProfileForm(request.user)

    return render(request, 'delete_profile.html', {'form': form})
