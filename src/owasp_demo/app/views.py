from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import RegisterForm, Profile, LoginForm, ProfileForm, UserSearchForm


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
            user = User.objects.create_user(username=username, password=password)
            user.save()
            Profile.objects.create(user=user, email=email, phone_number=phone_number)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {"form": form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('profile')
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})


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
                users = User.objects.filter(username__icontains=username)
            else:
                users = User.objects.all()
    else:
        form = UserSearchForm()
    return render(request, 'app/search_users.html', {'form': form, 'users': users})

@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'app/user_profile.html', {'user': user})
