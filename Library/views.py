from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user == None:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
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
    if request.method == 'POST':
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        roll_no = request.POST.get('roll_no')
        section = request.POST.get('section')
        teacher_id = request.POST.get('teacher_id')
        department = request.POST.get('department')
        if name != '' and class_id != '' and roll_no != '' and section != '':
            if Students.objects.filter(roll_no=roll_no).exists():
                messages. error(request, 'User already exists')
                return redirect('add_users')
            userinfo= Students(name=name, class_id=class_id, roll_no=roll_no, section=section)
        elif teacher_id != '' and department != '':
            if Teacher.objects.filter(teacher_id=teacher_id).exists():
                messages. error(request, 'User already exists')
                return redirect('add_users')
            userinfo= Teacher(name=name, teacher_id=teacher_id, department=department)
        else:
            messages. error(request, 'All fields are required')
            return redirect('add_users')
        userinfo.save()
        try:
            messages.success(request, 'User Added Successfully')
            return redirect('add_users')
        except:
            messages. error(request, 'Error in adding user')
            return redirect('add_users')
    return render(request, 'addusers.html')\

def Logout(request):
    logout(request)
    return render(request, 'login.html')