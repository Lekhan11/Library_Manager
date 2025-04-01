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
        print(new_category)
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
                bookInfo = Book.objects.create(
                title=book_name,
                author=author,
                isbn=isbn,
                publisher=publications,
                quantity=quantity
            )
           
                bookInfo.categories.set(category)
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

# View to handle book return
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
            returnBook = ReturnedBooks(user=user, book=Book.objects.get(isbn=book_id), return_date=return_date ,condition=book_condition)
            returnBook.save()
            if user.books_pending <= 0:
                messages.error(request, 'No books to return')
                return redirect('return_book')
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

def  viewBooks(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'view_books.html', {'books': books, 'categories': categories})

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

def deleteBook(request, id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        messages.success(request, 'Book Deleted Successfully')
    except:
        messages.error(request, 'Error in deleting book')
    return redirect('view_books')