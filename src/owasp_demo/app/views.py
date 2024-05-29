from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html')


def register(request):
    pass


def login(request):
    pass
