from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate, login
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        chk_user = authenticate(request, username=username, password=password)
        if chk_user.is_student:
            login(request,chk_user)
            return render(request, 'home.html')
        else:
            return render(request, 'login.html',context={'error':'Invalid Username or Password'})
    return render(request, 'login.html')