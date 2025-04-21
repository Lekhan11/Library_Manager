from multiprocessing import context
from turtle import title
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from random import sample
from django.core.paginator import Paginator
import csv
from django.http import JsonResponse
from datetime import datetime

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
    #books = Book.objects.filter(id__in=selected_ids)  # Fetch those books
    total_books = books.count()
    students = Students.objects.all()
    total_students = students.count()
    teachers = Teacher.objects.all()
    total_teachers = teachers.count()
    transaction = Transaction.objects.all()
    total_issued = transaction.filter(transaction_type='issue').count()
    total_returned = transaction.filter(transaction_type='return').count()
    total_pending = total_issued - total_returned
    issued_thisMonth = transaction.filter(date__month=datetime.now().month).count()
    returned_thisMonth = transaction.filter(date__month=datetime.now().month, transaction_type='return').count()
    pending_thisMonth = issued_thisMonth - returned_thisMonth
    context = {'total_books':total_books, 'total_students':total_students, 'total_teachers':total_teachers, 'total_issued':total_issued, 'total_returned':total_returned, 'total_pending':total_pending, 'issued_thisMonth':issued_thisMonth, 'returned_thisMonth':returned_thisMonth, 'pending_thisMonth':pending_thisMonth} 
    return render(request, 'home.html',context)

@login_required(login_url='login')
def IssueBooks(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        issue_date = request.POST.get('issue_date')
        due_date = request.POST.get('due_date')

        if user_id == '' or book_id == '' or issue_date == '' or due_date == '':
            messages.error(request, 'All fields are required')
            return redirect('issue_books')

        user = None
        user_model = None

        if Students.objects.filter(roll_no=user_id).exists():
            user = Students.objects.get(roll_no=user_id)
            user_model = Students
        elif Teacher.objects.filter(teacher_id=user_id).exists():
            user = Teacher.objects.get(teacher_id=user_id)
            user_model = Teacher
        else:
            messages.error(request, 'User not found')
            return redirect('issue_books')

        try:
            book = Book.objects.get(isbn=book_id)
        except Book.DoesNotExist:
            messages.error(request, 'Book not found')
            return redirect('issue_books')

        # Check for duplicate issue
        content_type = ContentType.objects.get_for_model(user_model)
        if IssuedBooks.objects.filter(content_type=content_type, object_id=user.id, book=book).exists():
            messages.error(request, 'Book already issued to this user')
            return redirect('issue_books')

        try:
            issued_book = IssuedBooks.objects.create(
                content_type=content_type,
                object_id=user.id,
                book=book,
                issue_date=issue_date,
                due_date=due_date
            )
            user.books_issued += 1
            user.books_pending += 1
            user.save()

            book.quantity -= 1
            book.save()
            transaction = Transaction(
                user=user,
                book=book,
                transaction_type='issue',
                date=issue_date
            )
            transaction.save()
            messages.success(request, 'Book Issued Successfully')
        except Exception as e:
            print("Error:", e)
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
            if Book.objects.filter(isbn=isbn).exists():
                messages.error(request, 'Book ID already exists')
                return redirect('add_book')
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
    setting_instance = Setting.objects.first()
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
    
    return render(request, 'addusers.html', {'settings': setting_instance})


@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def viewUsers(request):
    students_list = Students.objects.all()
    teachers_list = Teacher.objects.all()

    student_ct = ContentType.objects.get_for_model(Students)
    teacher_ct = ContentType.objects.get_for_model(Teacher)

    student_paginator = Paginator(students_list, 10)
    teacher_paginator = Paginator(teachers_list, 10)

    # Add book data to students
    for student in students_list:
        issued = IssuedBooks.objects.filter(content_type=student_ct, object_id=student.id)
        returned = ReturnedBooks.objects.filter(content_type=student_ct, object_id=student.id)
        returned_ids = [r.book.id for r in returned]
        pending = [b for b in issued if b.book.id not in returned_ids]
        student.books_returned = returned.count()
        student.books_pending = len(pending)
        student.pending_books = pending

    # Add book data to teachers
    for teacher in teachers_list:
        issued = IssuedBooks.objects.filter(content_type=teacher_ct, object_id=teacher.id)
        returned = ReturnedBooks.objects.filter(content_type=teacher_ct, object_id=teacher.id)
        returned_ids = [r.book.id for r in returned]
        pending = [b for b in issued if b.book.id not in returned_ids]
        teacher.books_returned = returned.count()
        teacher.books_pending = len(pending)
        teacher.pending_books = pending

    students = student_paginator.get_page(request.GET.get('student_page'))
    teachers = teacher_paginator.get_page(request.GET.get('teacher_page'))

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
            elif Teacher.objects.filter(teacher_id=teacher_id).exists():
                messages.error(request, 'User already exists')
                return redirect('view_users')
            else:
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
            elif Students.objects.filter(roll_no=roll_no).exists():
                messages.error(request, 'User already exists')
                return redirect('view_users')
            else:
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
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        return_date = request.POST.get('returnDate')
        book_condition = request.POST.get('condition')

        # Check if book exists
        if not Book.objects.filter(isbn=book_id).exists():
            messages.error(request, 'Book not found')
            return redirect('return_book')

        # Determine if the user is a Student or Teacher
        if Students.objects.filter(roll_no=user_id).exists():
            user = Students.objects.get(roll_no=user_id)
            content_type = ContentType.objects.get_for_model(Students)
        elif Teacher.objects.filter(teacher_id=user_id).exists():
            user = Teacher.objects.get(teacher_id=user_id)
            content_type = ContentType.objects.get_for_model(Teacher)
        else:
            messages.error(request, 'User not found')
            return redirect('return_book')

        # Validate the input fields
        if not user_id or not book_id or not return_date or not book_condition:
            messages.error(request, 'All fields are required')
            return redirect('return_book')

        # Check if the book is issued to this user
        issued_book = IssuedBooks.objects.filter(
            content_type=content_type,
            object_id=user.id,
            book=Book.objects.get(isbn=book_id)
        ).first()

        if not issued_book:
            messages.error(request, 'This book was not issued to this user')
            return redirect('return_book')

        # Calculate Fine based on the due date
        due_date = issued_book.due_date
        return_date_obj = datetime.strptime(return_date, "%Y-%m-%d").date()
        fine = 0

        if return_date_obj > due_date:
            settings = Setting.objects.first()
            if settings:
                if isinstance(user, Students):
                    fine = (return_date_obj - due_date).days * settings.fineStud
                else:
                    fine = (return_date_obj - due_date).days * settings.fineTeach

        # Save the returned book
        returned_book = ReturnedBooks(
            content_type=content_type,
            object_id=user.id,
            book=Book.objects.get(isbn=book_id),
            return_date=return_date,
            condition=book_condition
        )
        returned_book.save()

        # Update the issued book record (delete it)
        issued_book.delete()

        # Update the user's pending and returned books count
        
        user.books_pending -= 1
        user.books_returned += 1
        user.fine += fine  # Add fine if any
        user.save()

        # Update the book quantity (increment it)
        book = Book.objects.get(isbn=book_id)
        book.quantity += 1
        book.save()
        transaction = Transaction(
            user=user,
            book=book,
            transaction_type='return',
            date=return_date
        )
        transaction.save()

        messages.success(request, f"The book has been successfully returned! Fine: ₹{fine}")
        return redirect('return_book')

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

        # Check if student
        if Students.objects.filter(roll_no=user_id).exists():
            user = Students.objects.get(roll_no=user_id)
            ct = ContentType.objects.get_for_model(Students)

            issued_books = IssuedBooks.objects.filter(content_type=ct, object_id=user.id)
            returned_books = ReturnedBooks.objects.filter(content_type=ct, object_id=user.id)

            returned_book_ids = [r.book.id for r in returned_books]
            pending_books = [b for b in issued_books if b.book.id not in returned_book_ids]

            user.pending_books = pending_books
            user.books_returned = len(returned_books)
            user.books_pending = len(pending_books)
            # books_issued is stored in model directly

            return render(request, 'viewusers.html', {'searched_student': user})

        # Check if teacher
        elif Teacher.objects.filter(teacher_id=user_id).exists():
            user = Teacher.objects.get(teacher_id=user_id)
            ct = ContentType.objects.get_for_model(Teacher)

            issued_books = IssuedBooks.objects.filter(content_type=ct, object_id=user.id)
            returned_books = ReturnedBooks.objects.filter(content_type=ct, object_id=user.id)

            returned_book_ids = [r.book.id for r in returned_books]
            pending_books = [b for b in issued_books if b.book.id not in returned_book_ids]

            user.pending_books = pending_books
            user.books_returned = len(returned_books)
            user.books_pending = len(pending_books)
            # books_issued is stored in model directly

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
        elif Book.objects.filter(title=book_id).exists():
            book = Book.objects.get(title=book_id)
        elif Book.objects.filter(author=book_id).exists():
            book = Book.objects.get(author=book_id)
        else:
            messages.error(request, 'Book not found')
            return redirect('view_books')
        return render(request, 'view_books.html', {'searched_book': book})
    return redirect('view_books')

def bulkAdd(request):
    if request.method == "POST":
        role = request.POST.get("role")
        csv_file = request.FILES.get("csv_file")

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect('bulk_upload')

        reader = csv.reader(csv_file.read().decode('utf-8').splitlines())

        next(reader)  # Skip header

        for row in reader:
            if role == 'student':
                Students.objects.create(
                    name=row[0],
                    roll_no=row[1],
                    class_id=row[2],
                    section=row[3]
                )
            elif role == 'teacher':
                Teacher.objects.create(
                    teacher_id=row[1],
                    name=row[0],
                    department=row[2]
                )
        
        messages.success(request, f"{role.capitalize()}s added successfully.")
        return redirect('bulk_add')

    return render(request, 'bulkAdd.html')

import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, Category

def bulkAddBooks(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")

        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect('bulkadd_books')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader)  # Skip header row

            count = 0
            for row in reader:
                if len(row) < 6:
                    continue

                title = row[0].strip()
                author = row[1].strip()
                publisher = row[2].strip()
                quantity = int(row[3].strip())
                category_names = row[4].strip().split(',')
                isbn = row[6].strip()

                book = Book.objects.create(
                    title=title,
                    author=author,
                    publisher=publisher,
                    quantity=quantity,
                    isbn=isbn,
                    availability_status='Available'
                )

                for cat_name in category_names:
                    category, _ = Category.objects.get_or_create(name=cat_name.strip())
                    book.categories.add(category)

                count += 1

            messages.success(request, f"Successfully added {count} books.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('bulkadd_books')

    return render(request, 'bulkadd_books.html')


def settings_view(request):
    setting_instance = Setting.objects.first()  # Get the first (or only) row

    if request.method == 'POST':
        maxDueStud = request.POST.get('maxDueStud')
        maxDueTeach = request.POST.get('maxDueTeach')
        fineStud = request.POST.get('fineStud')
        fineTeach = request.POST.get('fineTeach')
        logo = request.FILES.get('logo')

        if '' in [maxDueStud, maxDueTeach, fineStud, fineTeach]:
            messages.error(request, 'All fields are required')
            return redirect('settings')
      

            messages.success(request, 'Logo Updated Successfully')
        # If no settings row exists, create one
        if not setting_instance:
            setting_instance = Setting.objects.create(
                maxDueStud=maxDueStud,
                maxDueTeach=maxDueTeach,
                fineStud=fineStud,
                fineTeach=fineTeach
            )
        else:
            # Update the existing row
            setting_instance.maxDueStud = maxDueStud
            setting_instance.logo = logo
            setting_instance.maxDueTeach = maxDueTeach
            setting_instance.fineStud = fineStud
            setting_instance.fineTeach = fineTeach
            setting_instance.save()

        messages.success(request, 'Settings Updated Successfully')
        return redirect('settings')

    return render(request, 'settings.html', {'settings': setting_instance})


def get_book_details(request):
    book_id = request.GET.get('book_id')  # Get the book_id (or ISBN) from the GET request
    if book_id:
        # Try to get the book based on the book_id (or ISBN)
        book = Book.objects.filter(isbn=book_id).first()
        if book:
            # Return book details as a JSON response
            book_details = {
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'quantity': book.quantity,
            }
            return JsonResponse({'success': True, 'book_details': book_details})
        else:
            return JsonResponse({'success': False, 'message': 'Book not found'})
    else:
        return JsonResponse({'success': False, 'message': 'No book ID provided'})



def get_user_role_due(request):
    user_id = request.GET.get('user_id')
    settings = Setting.objects.first()
    response = {}

    if Students.objects.filter(roll_no=user_id).exists():
        response['role'] = 'student'
        response['due_days'] = settings.maxDueStud
    elif Teacher.objects.filter(teacher_id=user_id).exists():
        response['role'] = 'teacher'
        response['due_days'] = settings.maxDueTeach
    else:
        response['role'] = 'unknown'
        response['due_days'] = 0

    return JsonResponse(response)

from django.http import JsonResponse

def get_fine(request):
    user_id = request.GET.get('user_id')
    book_id = request.GET.get('book_id')
    return_date = request.GET.get('return_date')

    if not user_id or not book_id or not return_date:
        return JsonResponse({'success': False, 'message': 'Missing parameters'})

    try:
        # Check if the user is a Student or Teacher and set the appropriate ContentType
        student_content_type = ContentType.objects.get_for_model(Students)
        teacher_content_type = ContentType.objects.get_for_model(Teacher)

        # Try to find the user as either Student or Teacher
        if Students.objects.filter(roll_no=user_id).exists():
            user = Students.objects.get(roll_no=user_id)
            user_content_type = student_content_type
        elif Teacher.objects.filter(teacher_id=user_id).exists():
            user = Teacher.objects.get(teacher_id=user_id)
            user_content_type = teacher_content_type
        else:
            return JsonResponse({'success': False, 'message': 'User not found'})

        # Get the book
        try:
            book = Book.objects.get(isbn=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Book not found'})

        # Get the issued book record for the user and book combination
        issued_book = IssuedBooks.objects.filter(
            content_type=user_content_type,
            object_id=user.id,
            book=book
        ).first()

        if not issued_book:
            return JsonResponse({'success': False, 'message': 'This book is not issued to the user'})

        # Get the fine settings
        setting = Setting.objects.first()
        if not setting:
            return JsonResponse({'success': False, 'message': 'Settings not found'})

        # Calculate fine
        fine = 0
        try:
            return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid date format, expected YYYY-MM-DD'})

        due_date_obj = issued_book.due_date

        # Debugging: print out due_date and return_date for comparison
        print(f"Due Date: {due_date_obj}, Return Date: {return_date_obj}")

        # Calculate the fine if the book is returned late
        if return_date_obj > due_date_obj:
            days_late = (return_date_obj - due_date_obj).days
            fine = days_late * (setting.fineStud if isinstance(user, Students) else setting.fineTeach)

            # Debugging: print out the fine calculation
            print(f"Days Late: {days_late}, Fine: {fine}")

        # Return fine in response
        return JsonResponse({'success': True, 'fine': fine})

    except Exception as e:
        # Debugging: print the exception error
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'message': str(e)})