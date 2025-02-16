from django.shortcuts import render
from .models import *
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        chk_user = User.objects.filter(username=username,password=password)
        if chk_user:
            return render(request, 'home.html')
        else:
            return render(request, 'login.html',context={'error':'Invalid Username or Password'})
    return render(request, 'login.html')