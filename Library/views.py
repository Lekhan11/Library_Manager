from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from random import sample
from django.core.paginator import Paginator

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user == None:
            messages.error(request, 'Invalid Username or password')
            return redirect('login')
        elif user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})

    return render(request, 'login.html')

@login_required(login_url='login')
def HomePage(request):
    books = Book.objects.all()
    
    book_ids = list(Book.objects.values_list('id', flat=True))  # Get all book IDs
    selected_ids = sample(book_ids, min(len(book_ids), 6))  # Pick 5 random IDs
    books = Book.objects.filter(id__in=selected_ids)  # Fetch those books
    total_books = books.count()
    students = Students.objects.all()
    total_students = students.count()
    teachers = Teacher.objects.all()
    total_teachers = teachers.count()
    context = {'total_books':total_books, 'total_students':total_students, 'total_teachers':total_teachers,'books':books} 
    return render(request, 'home.html',context)

@login_required(login_url='login')
def IssueBooks(request):
    if request.method=='POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        issue_date = request.POST.get('issue_date')
        due_date = request.POST.get('due_date')
        if user_id == '' or book_id == '' or issue_date == '' or due_date == '':
            messages.error(request, 'All fields are required')
            return redirect('issue_books')
        if Students.objects.filter(roll_no=user_id).exists():
            user = Students.objects.get(roll_no=user_id)
           
        elif Teacher.objects.filter(teacher_id=user_id).exists():
            user = Teacher.objects.get(teacher_id=user_id)
        
        else:
            messages.error(request, 'User not found')
            return redirect('issue_books')
        if Book.objects.filter(isbn=book_id).exists():
            book = Book.objects.get(isbn=book_id)
        else:
            messages.error(request, 'Book not found')
            return redirect('issue_books')
        if IssuedBooks.objects.filter(user=user, book=book).exists():
            messages.error(request, 'Book already issued to this user')
            return redirect('issue_books')
        try:
            issued_book = IssuedBooks(user=user, book=book, issue_date=issue_date, due_date=due_date)
            issued_book.save()
            user.books_issued = user.books_issued + 1
            user.books_pending = user.books_pending + 1
            user.save()
            book.quantity = book.quantity - 1
            book.save()
            messages.success(request, 'Book Issued Successfully')
        except:
            messages.error(request, 'Error in issuing book')
    return render(request, 'issue_books.html')
    
@login_required(login_url='login')
def addBook(request):
    context = {
        'categories': Category.objects.all()
    }
    if request.method=="POST":
        book_name=request.POST.get('book_name')
        author=request.POST.get('author')
        isbn=request.POST.get('isbn_code')
        publications=request.POST.get('publications')
        quantity=request.POST.get('quantity')
        new_category=request.POST.get('new_category')
        category = request.POST.get('category')
        print(category)
        if new_category:
            if Category.objects.filter(name=new_category).exists():
                messages. error(request, 'Category already exists')
                return redirect('add_book')
            else:
                categoryInfo = Category(name=new_category)
                categoryInfo.save()
                messages.error(request, 'Category Added Succesfully')
                return redirect('add_book')
        elif all([book_name, author, isbn, publications, quantity, category]):
            if Book.objects.filter(isbn=isbn).exists():
                messages. error(request, 'Book ID already exists')
                return redirect('add_book')
        try:
            category_obj = Category.objects.get(id=category)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category selected')
            return redirect('add_book')
        try:
            bookInfo = Book.objects.create(
                title=book_name,
                author=author,
                isbn=isbn,
                publisher=publications,
                quantity=quantity
        )
        
            bookInfo.categories.add(category_obj)
            messages.success(request, 'Book Added Successfully')
            return redirect('add_book')
        except Exception as e:
            print(e)
            messages.error(request, 'Error in adding book')
            return redirect('add_book')
        else:
            messages. error(request, 'All fields are required')
            return redirect('add_book')
    return render(request, 'addbooks.html',context)

@login_required(login_url='login')
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
        try:
            userinfo.save()
            messages.success(request, 'User Added Successfully')
            return redirect('add_users')
        except:
            messages. error(request, 'Error in adding user')
            return redirect('add_users')
    
    return render(request, 'addusers.html')


@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def viewUsers(request):
    students_list = Students.objects.all()
    teachers_list = Teacher.objects.all()
    books_issued = IssuedBooks.objects.all()
    books_returned = ReturnedBooks.objects.all()
    student_paginator = Paginator(students_list, 2)  # 5 per page
    teacher_paginator = Paginator(teachers_list, 2)

    for student in students_list:
        student_issued_books = IssuedBooks.objects.filter(user=student)
        student_returned_books = ReturnedBooks.objects.filter(user=student)
        returned_book_ids = [r.book.id for r in student_returned_books]
        pending_books = [b for b in student_issued_books if b.book.id not in returned_book_ids]
        student.pending_books = pending_books
           
    student_page_number = request.GET.get('student_page')
    teacher_page_number = request.GET.get('teacher_page')

    students = student_paginator.get_page(student_page_number)
    teachers = teacher_paginator.get_page(teacher_page_number)

    context = {
        'students': students,
        'teachers': teachers,
        
        
    }
    return render(request, 'viewusers.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

# View to handle book return
@login_required(login_url='login')
def returnBook(request):
    if request.method == "POST":
        # Retrieve form dat
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        return_date = request.POST.get('returnDate')
        book_condition = request.POST.get('condition')
        if not Book.objects.filter(isbn=book_id).exists():
            messages.error(request, 'Book not found')
            return redirect('return_book')
        if Students.objects.filter(roll_no=user_id).exists():
            user = Students.objects.get(roll_no=user_id)
        elif Teacher.objects.filter(teacher_id=user_id).exists():
            user = Teacher.objects.get(teacher_id=user_id)
        else:
            messages.error(request, 'User not found')
            return redirect('return_book')
        if user_id == '' or book_id == '' or return_date == '' or book_condition == '':
            messages.error(request, 'All fields are required')
            return redirect('return_book')
        else:
            issued_book = IssuedBooks.objects.filter(user=user.id, book=Book.objects.get(isbn=book_id)).first()
            if not issued_book:
                messages.error(request, 'Book not issued to this user')
                return redirect('return_book')
            elif user.books_pending <= 0:
                messages.error(request, 'No books to return')
                return redirect('return_book')
            else:
                returnBook = ReturnedBooks(user=user, book=Book.objects.get(isbn=book_id), return_date=return_date ,condition=book_condition)
                returnBook.save()
                issued_book.delete()
                user.books_pending = user.books_pending - 1
                user.books_returned = user.books_returned + 1
                user.save()
                book = Book.objects.get(isbn=book_id)
                book.quantity = book.quantity + 1
                book.save()
                messages.success(request, "The book has been successfully returned!")
                return redirect('return_book')

        # Redirect to the same page with a success message
        return render(request, 'returnBook.html')
    else:
        return render(request, 'returnBook.html')

@login_required(login_url='login')
def  viewBooks(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'view_books.html', {'books': books, 'categories': categories})

@login_required(login_url='login')
def updateBook(request,id):
    if request.method == 'POST':
        book_name = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        publications = request.POST.get('publisher')
        quantity = request.POST.get('quantity')
        if book_name == '' or author == '' or isbn == '' or publications == '' or quantity == '':
            messages.error(request, 'All fields are required')
            return redirect('view_books')

        if Book.objects.filter(isbn=isbn).exclude(id=id).exists():
            messages.error(request, 'Book ID already exists')
            return redirect('view_books')

        if Book.objects.filter(id=id).exists():
            bookInfo = Book.objects.get(id=id)
            bookInfo.title = book_name
            bookInfo.author = author
            bookInfo.isbn = isbn
            bookInfo.publisher = publications
            bookInfo.quantity = quantity
            bookInfo.save()
            messages.success(request, 'Book Updated Successfully')
            return redirect('view_books')
        else:
            messages.error(request, 'Book not found')
            return redirect('view_books')

@login_required(login_url='login')

def deleteBook(request, id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        messages.success(request, 'Book Deleted Successfully')
    except:
        messages.error(request, 'Error in deleting book')
    return redirect('view_books')

@login_required(login_url='login')
def searchUser(request):
    if request.method == 'POST':
        user_id = request.POST.get('userID')
        
        if Students.objects.filter(roll_no=user_id).exists():
            user = Students.objects.get(roll_no=user_id)
            student_issued_books = IssuedBooks.objects.filter(user=user)
            student_returned_books = ReturnedBooks.objects.filter(user=user)
            returned_book_ids = [r.book.id for r in student_returned_books]
            pending_books = [b for b in student_issued_books if b.book.id not in returned_book_ids]
            user.pending_books = pending_books
            return render(request, 'viewusers.html', {'searched_student': user})
        elif Teacher.objects.filter(teacher_id=user_id).exists():
            user = Teacher.objects.get(teacher_id=user_id)
            return render(request, 'viewusers.html', {'searched_teacher': user})
        else:
            messages.error(request, 'User not found')
            return redirect('view_users')
    return redirect('view_users')

def searchBook(request):
    if request.method == 'POST':
        book_id = request.POST.get('bookID')
        if Book.objects.filter(isbn=book_id).exists():
            book = Book.objects.get(isbn=book_id)
            return render(request, 'view_books.html', {'searched_book': book})
        else:
            messages.error(request, 'Book not found')
            return redirect('view_books')
    return redirect('view_books')

def bulkAdd(request):
    return render(request, 'bulkadd.html')