from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user == None:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})
        elif user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})

    return render(request, 'login.html')

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')