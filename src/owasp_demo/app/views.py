import logging
import traceback

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import RegisterForm, Profile, LoginForm, ProfileForm, UserSearchForm


logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'app/index.html')


def register(request):  # A09:2021: No logging
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            user = User(username=username)
            # A02:2021: Passwords stored in plain text
            # A07:2021: Permits weak passwords, Passwords stored in plain text
            user.password = password
            user.save()
            Profile.objects.create(user=user, email=email, phone_number=phone_number, password=password)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {"form": form})


@csrf_exempt
def login(request):  # A09:2021: Logins and failed login are not logged
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.get(username=username)
                if user.profile.password == password:
                    auth_login(request, user)
                    return redirect('profile')
                else:  # A05:2021: Error case reveals overly informative error messages to user
                    return HttpResponse("Invalid login. Your username or password was wrong.")
        else:
            form = LoginForm()
        return render(request, 'app/login.html', {'form': form})
    except Exception as e:
        # A05:2021: Error handling reveals stack traces
        return HttpResponse(f"Error: {str(e)}<br>{traceback.format_exc()}")


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
            if username:  # A03:2021: SQL Injection vulnerability
                query = f"""
                    SELECT * FROM auth_user 
                    WHERE username LIKE '%{username}%' 
                    AND id IN (
                        SELECT user_id 
                        FROM app_profile 
                        WHERE is_public = 1
                    )
                """
                users = User.objects.raw(query)
            else:
                query = """
                    SELECT * FROM auth_user 
                    WHERE id IN (
                        SELECT user_id 
                        FROM app_profile 
                        WHERE is_public = 1
                    )
                """
                users = User.objects.raw(query)

    else:
        form = UserSearchForm()
    return render(request, 'app/search_users.html', {'form': form, 'users': users})


@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)  # A01:2021: No access control checks
    return render(request, 'app/user_profile.html', {'user': user})
