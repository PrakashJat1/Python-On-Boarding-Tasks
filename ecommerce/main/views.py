from django.shortcuts import render
from django.contrib.auth import logout


def home(request):
    # logout(request)
    return render(request, "Home.html")
