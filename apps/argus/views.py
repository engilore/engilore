from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from argus.forms import UserRegisterForm, UserLoginForm
from account.models import User


def argus_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.check_and_set_admin_status()
            user.save()
            messages.success(request, 'Your account has been created successfully.')
            login(request, user)
            return redirect('core-home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    context = {'form': form, 'title': 'Join'}
    return render(request, 'argus_templates/views/argus_register.html', context)


def argus_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email__iexact=username_or_email)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(username__iexact=username_or_email)
                except User.DoesNotExist:
                    user = None

            if user:
                user = authenticate(username=user.username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('core-home')
            messages.error(request, 'Invalid username/email or password.')
    else:
        form = UserLoginForm()

    context = {'form': form, 'title': 'Login'}
    return render(request, 'argus_templates/views/argus_login.html', context)

def argus_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core-home')