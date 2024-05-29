from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import RegisterForm, Profile, LoginForm


def index(request):
    return render(request, 'app/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            Profile.objects.create(user=user, email=request.POST['email'])
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
                login(request)
                return redirect('profile')  # TODO
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})
