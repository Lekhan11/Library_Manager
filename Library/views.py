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
    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def _str_(self):
        return f"{self.book.title} issued to {self.student.user.get_full_name()}"
    
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
    return redirect('login')

def viewUsers(request):
    students = Students.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'viewusers.html', {'students': students, 'teachers': teachers})

def deleteUser(request, id):
    try:
        user = Students.objects.get(id=id)
        user.delete()
        messages.success(request, 'User Deleted Successfully')
    except:
        messages.error(request, 'Error in deleting user')
    return redirect('view_users')