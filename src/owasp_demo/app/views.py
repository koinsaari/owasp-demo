# Copyright (c) 2024 Aaro Koinsaari
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import logging

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import RegisterForm, Profile, LoginForm, ProfileForm, UserSearchForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'app/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            user = User(username=username)
            try:
                validate_password(password, user)
                user.set_password(password)
                user.save()
                Profile.objects.create(user=user, email=email, phone_number=phone_number)
                logger.info(f"New user registered: {username}")
                return redirect('login')
            except ValidationError as e:
                form.add_error('password', e)
                logger.warning(f"Password validation failed for user {username}: {e}")
        else:
            logger.warning("Registration form was invalid.")
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {"form": form})


@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    logger.info(f"User logged in: {username}")
                    return redirect('profile')
                else:
                    logger.warning(f"Invalid login attempt for user: {username}")
                    return HttpResponse("Invalid login. Please try again.")
        else:
            form = LoginForm()
        return render(request, 'app/login.html', {'form': form})
    except Exception as e:
        logger.error(f"An error occurred during login: {str(e)}")
        return HttpResponse("An error has occurred. Please try again later.")


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user.profile)
    return render(request, 'app/profile.html', {'form': form})


@login_required
def search_users(request):
    users = []
    if request.method == 'GET':
        form = UserSearchForm(request.GET)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if username:
                users = User.objects.filter(username__icontains=username, profile__is_public=True)
            else:
                users = User.objects.filter(profile__is_public=True)
    else:
        form = UserSearchForm()
    return render(request, 'app/search_users.html', {'form': form, 'users': users})


@login_required
def user_profile(request, user_id):
    if request.user.id != user_id:
        return HttpResponse("Unauthorized access.", status=403)
    user = User.objects.get(id=user_id)
    return render(request, 'app/user_profile.html', {'user': user})
