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

@login_required(login_url='login')
def IssueBooks(request):
    context = {
        'books': Book.objects.all(),
        'students': StudentExtra.objects.all(),
        'categories': Category.objects.all()
    }
    if request.method=='POST':
        roll_no = request.POST.get('roll_no')
        id = request.POST.get('book_id')
        issue_date = request.POST.get('issue_date')
        due_date = request.POST.get('due_date')
        save_issue = IssuedBooks(user=roll_no, book=id, issue_date=issue_date, due_date=due_date)  
        save_issue.save()   
        return render(request, 'issue_books.html', {'message': 'Book Issued Successfully'})
    return render(request, 'issue_books.html', context)
    
def updateUser(request):
    return render(request, 'update.html')

def addBook(request):
    return render(request, 'addbooks.html')

def addusers(request):
    return render(request, 'addusers.html')