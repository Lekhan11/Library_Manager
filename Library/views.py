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
    return redirect('login')

def viewUsers(request):
    students = Students.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'viewusers.html', {'students': students, 'teachers': teachers})

def deleteUser(request, role,id):
    try:
        if role == 'teacher':
            user = Teacher.objects.get(id=id)
        else:
            user = Students.objects.get(id=id)
        user.delete()
        messages.success(request, 'User Deleted Successfully')
    except:
        messages.error(request, 'Error in deleting user')
    return redirect('view_users')

def updateUser(request,role,id):
    if role == 'teacher':
        user = Teacher.objects.get(id=id)
        if request.method == 'POST':
            name = request.POST.get('name')
            teacher_id = request.POST.get('teacher_id')
            department = request.POST.get('department')
            if name == '' or teacher_id == '' or department == '':
                messages.error(request, 'All fields are required')
                return redirect('view_users')
            user.name = name
            user.teacher_id = teacher_id
            user.department = department
            user.save()
            messages.success(request, 'User Updated Successfully')
        return redirect('view_users')
    else:
        user = Students.objects.get(id=id)
        if request.method == 'POST':
            name = request.POST.get('name')
            class_id = request.POST.get('class_id')
            roll_no = request.POST.get('roll_no')
            print(request.POST)
            section = request.POST.get('section')
            if name == '' or class_id == '' or roll_no == '' or section == '':
                messages.error(request, 'All fields are required')
                return redirect('view_users')
            user.name = name
            user.class_id = class_id
            user.roll_no = roll_no
            user.section = section
            user.save()
            messages.success(request, 'User Updated Successfully')
        return redirect('view_users')
    return redirect('view_users')
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

# View to handle book return
def returnBook(request):
    if request.method == "POST":
        # Retrieve form data
        student_id = request.POST.get('studentId')
        book_id = request.POST.get('bookId')
        return_date = request.POST.get('returnDate')
        book_condition = request.POST.get('bookCondition')

        # You can now process the return (e.g., update the database, check conditions, etc.)
        # For example, check if the book exists in the library system
        # and update the database to mark it as returned.

        # Assume the return is successful (you should add your actual logic)
        messages.success(request, "The book has been successfully returned!")

        # Redirect to the same page with a success message
        return render(request, 'returnBook.html')
    else:
        return render(request, 'returnBook.html')



