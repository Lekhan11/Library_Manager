from multiprocessing import context
import re
from turtle import pen, title
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
from datetime import timedelta
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType


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
    issued_thisMonth = transaction.filter(date__month=datetime.now().month,transaction_type='issue').count()
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
        print(issue_date)
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
            book = Accession_No.objects.get(accession_no=book_id)
            if book.quantity <= 0:
                messages.error(request, 'Book not available')
                return redirect('issue_books')
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
        isbn=request.POST.get('isbn')
        publications=request.POST.get('publications')
        quantity=request.POST.get('quantity')
        new_category=request.POST.get('new_category')
        category = request.POST.get('category')
        accession_no = request.POST.get('book_id')
        if new_category:
            if Category.objects.filter(name=new_category).exists():
                messages. error(request, 'Category already exists')
                return redirect('add_book')
            else:
                categoryInfo = Category(name=new_category)
                categoryInfo.save()
                messages.error(request, 'Category Added Succesfully')
                return redirect('add_book')
        elif all([book_name, author, publications, category, accession_no]):
            if Accession_No.objects.filter(accession_no=accession_no).exists():
                messages. error(request, 'Accession number already exists')
                return redirect('add_book')
            try:
                category_obj = Category.objects.get(id=category)
            except Category.DoesNotExist:
                messages.error(request, 'Invalid category selected')
                return redirect('add_book')
            try:
                if Accession_No.objects.filter(accession_no=accession_no).exists():
                    messages.error(request, 'Accession Number already exists')
                    return redirect('add_book')
                
                if Book.objects.filter(title=book_name, author=author, isbn=isbn).exists():
                    pass
                else:
                    bookInfo = Book.objects.create(
                        title=book_name,
                        author=author,
                        isbn=isbn,
                        publisher=publications,
                        availability_status='Available',
                    )
                    bookInfo.categories.add(category_obj)
                bookDetail = Book.objects.get(title=book_name, author=author, isbn=isbn)
                Accession_No.objects.create(
                        accession_no=accession_no,
                        book_id=bookDetail
                )
                bookDetail.quantity += int(quantity)
                bookDetail.save()
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
        
        # Track the ids of returned books
        returned_ids = [r.book.id for r in returned]
        
        # List comprehension to get the pending books
        student.pending_books = [b.book for b in issued if b.book.id not in returned_ids]
        
        # Count pending books including any re-issued ones after return
        student.pending_books_count = len(student.pending_books)
        
        # Add logic for re-issued books if necessary
        reissued_books = [b.book for b in issued if b.book.id in returned_ids]
        student.pending_books.extend(reissued_books)
        print(set(student.pending_books))
        # Remove duplicates if a book was returned and re-issued (so it appears only once)
        student.pending_books = list(set(student.pending_books))
    # Add book data to teachers
    for teacher in teachers_list:
        issued = IssuedBooks.objects.filter(content_type=teacher_ct, object_id=teacher.id)
        returned = ReturnedBooks.objects.filter(content_type=teacher_ct, object_id=teacher.id)
        
        # Track the ids of returned books
        returned_ids = [r.book.id for r in returned]
        
        # List comprehension to get the pending books
        teacher.pending_books = [b.book for b in issued if b.book.id not in returned_ids]
        
        # Count pending books including any re-issued ones after return
        teacher.pending_books_count = len(teacher.pending_books)
        
        # Add logic for re-issued books if necessary
        reissued_books = [b.book for b in issued if b.book.id in returned_ids]
        teacher.pending_books.extend(reissued_books)
        print(set(teacher.pending_books))
        # Remove duplicates if a book was returned and re-issued (so it appears only once)
        teacher.pending_books = list(set(teacher.pending_books))
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
            elif Teacher.objects.filter(teacher_id=teacher_id,name=name,department=department).exists():
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
            elif Students.objects.filter(roll_no=roll_no,name=name,class_id=class_id,section=section).exists():
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
    date = datetime.now()
    current_date = date.strftime("%Y-%m-%d")
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        return_date = request.POST.get('returnDate')
        book_condition = request.POST.get('condition')

        # Check if book exists
        if not Accession_No.objects.filter(accession_no=book_id).exists():
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
            book=Accession_No.objects.get(accession_no=book_id)
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
            book=Accession_No.objects.get(accession_no=book_id),
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
        book = Accession_No.objects.get(accession_no=book_id)
        book.quantity += 1
        book.save()
        transaction = Transaction(
    user=user,
    book=book,
    transaction_type='return',
    date=datetime.combine(return_date_obj, datetime.min.time())  # at 00:00 time
)
        transaction.save()

        messages.success(request, f"The book has been successfully returned! Fine: ₹{fine}")
        return redirect('return_book')

    return render(request, 'returnBook.html',{'date':current_date})

@login_required(login_url='login')
def  viewBooks(request):
    books = Book.objects.all()
    accession_no = Accession_No.objects.all()
    categories = Category.objects.all()
    return render(request, 'view_books.html', {'books': books, 'categories': categories, 'accession_no': accession_no})

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

        if Book.objects.filter(title=book_name,author=author).exclude(id=id).exists() or Book.objects.filter(isbn=isbn).exclude(id=id).exists():
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
        if Students.objects.filter(roll_no__icontains=user_id).exists():
            user = Students.objects.get(roll_no__icontains=user_id)
            ct = ContentType.objects.get_for_model(Students)

            issued = IssuedBooks.objects.filter(content_type=ct, object_id=user.id)
            returned = ReturnedBooks.objects.filter(content_type=ct, object_id=user.id)
        
        # Track the ids of returned books
            returned_ids = [r.book.id for r in returned]
        
        # List comprehension to get the pending books
            user.pending_books = [b.book for b in issued if b.book.id not in returned_ids]

        # Count pending books including any re-issued ones after return
            user.pending_books_count = len(user.pending_books)
        
        # Add logic for re-issued books if necessary
            reissued_books = [b.book for b in issued if b.book.id in returned_ids]
            user.pending_books.extend(reissued_books)
            print(set(user.pending_books))
        # Remove duplicates if a book was returned and re-issued (so it appears only once)
            user.pending_books = list(set(user.pending_books))

            return render(request, 'viewusers.html', {'searched_student': user})

        # Check if teacher
        elif Teacher.objects.filter(teacher_id__icontains=user_id).exists():
            user = Teacher.objects.get(teacher_id__icontains=user_id)
            ct = ContentType.objects.get_for_model(Teacher)

            issued = IssuedBooks.objects.filter(content_type=ct, object_id=user.id)
            returned = ReturnedBooks.objects.filter(content_type=ct, object_id=user.id)
        
        # Track the ids of returned books
            returned_ids = [r.book.id for r in returned]
        
        # List comprehension to get the pending books
            user.pending_books = [b.book for b in issued if b.book.id not in returned_ids]
        
        # Count pending books including any re-issued ones after return
            user.pending_books_count = len(user.pending_books)
        
        # Add logic for re-issued books if necessary
            reissued_books = [b.book for b in issued if b.book.id in returned_ids]
            user.pending_books.extend(reissued_books)
            print(set(user.pending_books))
        # Remove duplicates if a book was returned and re-issued (so it appears only once)
            user.pending_books = list(set(user.pending_books))
            return render(request, 'viewusers.html', {'searched_teacher': user})

        else:
            messages.error(request, 'User not found')
            return redirect('view_users')

    return redirect('view_users')


def searchBook(request):
    if request.method == 'POST':
        bookid = request.POST.get('bookID')
        book = None

        if Accession_No.objects.filter(accession_no=bookid).exists():
            book = Accession_No.objects.get(accession_no=bookid)
        elif Accession_No.objects.filter(book_id__title__icontains=bookid).exists():
            book = Accession_No.objects.filter(book_id__title__icontains=bookid).first()
        elif Accession_No.objects.filter(book_id__author__icontains=bookid).exists():
            book = Accession_No.objects.filter(book_id__author__icontains=bookid).first()
        else:
            messages.error(request, 'Book not found')
            return redirect('view_books')

        book.access = Accession_No.objects.filter(book_id=book.book_id)
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
        book = Accession_No.objects.filter(accession_no=book_id).first()
        avail =  'Available' if book.quantity > 0 else 'Not Available'
        if book:
            # Return book details as a JSON response
            book_details = {
                'title': book.book_id.title,
                'author': book.book_id.author,
                'isbn': book.book_id.isbn,
                'quantity': book.book_id.quantity,
                'availability_status': avail,
                
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

from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from .models import Students, Teacher, Accession_No, IssuedBooks, Setting

def get_fine(request):
    user_id = request.GET.get('user_id', '').strip()
    book_id = request.GET.get('book_id', '').strip()
    return_date = request.GET.get('return_date', '').strip()

    if not user_id or not book_id or not return_date:
        return JsonResponse({'success': False, 'message': 'Missing parameters'})

    try:
        # 1. Get user (Student or Teacher)
        user = None
        user_content_type = None

        if Students.objects.filter(roll_no__iexact=user_id).exists():
            user = Students.objects.get(roll_no__iexact=user_id)
            user_content_type = ContentType.objects.get_for_model(Students)
            print(f"Found Student: {user}")
        elif Teacher.objects.filter(teacher_id__iexact=user_id).exists():
            user = Teacher.objects.get(teacher_id__iexact=user_id)
            user_content_type = ContentType.objects.get_for_model(Teacher)
            print(f"Found Teacher: {user}")
        else:
            return JsonResponse({'success': False, 'message': 'User not found'})

        # 2. Get Accession_No instance (Book copy)
        try:
            book = Accession_No.objects.get(accession_no__iexact=book_id)
            print(f"Found Book: {book}")
        except Accession_No.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Book not found'})

        # 3. Find issued record
        issued_book = IssuedBooks.objects.filter(
            content_type=user_content_type,
            object_id=user.id,
            book=book
        ).first()

        if not issued_book:
            return JsonResponse({'success': False, 'message': 'This book is not issued to the user'})

        print(f"Issued Book Record: {issued_book}")

        # 4. Get settings
        setting = Setting.objects.first()
        if not setting:
            return JsonResponse({'success': False, 'message': 'Settings not found'})

        # 5. Fine calculation
        try:
            return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD.'})

        due_date_obj = issued_book.due_date
        print(f"Due Date: {due_date_obj}, Return Date: {return_date_obj}")

        fine = 0
        if return_date_obj > due_date_obj:
            days_late = (return_date_obj - due_date_obj).days
            fine_per_day = setting.fineStud if isinstance(user, Students) else setting.fineTeach
            fine = days_late * fine_per_day
            print(f"Days Late: {days_late}, Fine Per Day: {fine_per_day}, Total Fine: {fine}")

        return JsonResponse({'success': True, 'fine': fine})

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})



def fine(request): # Fetch all fines from the database

    # This line should also be indented correctly
    return render(request, 'fine.html', {'fines': fine})

def report(request):
    return render(request,'report.html')
    return render(request, 'fine.html')

def get_user_fine(request):
    user_id = request.GET.get('user_id')
    
    # First check in Students
    student = Students.objects.filter(roll_no=user_id).first()
    if student:
        return JsonResponse({
            'success': True,
            'role': 'Student',
            'name': student.name,
            'fine': student.fine
        })
    
    # If not in Students, check in Teachers
    teacher = Teacher.objects.filter(teacher_id=user_id).first()
    if teacher:
        return JsonResponse({
            'success': True,
            'role': 'Teacher',
            'name': teacher.name,
            'fine': teacher.fine
        })

    # If not found in both
    return JsonResponse({'success': False, 'message': 'User not found'})

import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def pay_user_fine(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        role = data.get("role")
        amount_paid = int(data.get("amount_paid", 0))

        if role == "Student":
            user = Students.objects.filter(roll_no=user_id).first()
        elif role == "Teacher":
            user = Teacher.objects.filter(teacher_id=user_id).first()
        else:
            return JsonResponse({'success': False, 'message': 'Invalid role'})

        if user:
            old_fine = user.fine
            user.fine = user.fine - amount_paid
            user.save()
            return JsonResponse({
                'success': True,
                'message': f'₹{amount_paid} fine paid successfully. Previous: ₹{old_fine}, Now: ₹{user.fine}',
                'new_fine': user.fine
            })

        return JsonResponse({'success': False, 'message': 'User not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})



def report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        transacType = request.POST.get('type')
        action = request.POST.get('action')  # To detect Filter or Export

        if start_date and end_date and transacType:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            end_date_obj = end_date_obj + timedelta(days=1)  # include full day

            books = Transaction.objects.filter(
                transaction_type=transacType,
                date__range=[start_date_obj, end_date_obj]
            )

            if transacType == 'late_return':
                late_returns = []
                returned_books_qs = ReturnedBooks.objects.filter(
                    return_date__range=[start_date_obj, end_date_obj]
                )

                for record in returned_books_qs:
                    issue_txn = Transaction.objects.filter(
                        transaction_type='issue',
                        book=record.book,
                        content_type=ContentType.objects.get_for_model(record.user),
                        object_id=record.user.id,
                        date__lte=record.return_date
                    ).order_by('-date').first()

                    if issue_txn:
                        issue_date = issue_txn.date.date()
                        due_date = issue_date + timedelta(days=15)

                        if record.return_date > due_date:
                            days_late = (record.return_date - due_date).days
                            late_returns.append({
                                'user': record.user,
                                'book': record.book,
                                'return_date': record.return_date,
                                'due_date': due_date,
                                'days_late': days_late
                            })

                # Handle Export action
                if action == 'export':
                    return export_late_returns_csv(late_returns, start_date, end_date)

                context = {
                    'books': books,
                    'late_returns': late_returns,
                    'start_date': start_date,
                    'end_date': end_date,
                    'type': transacType
                }
                return render(request, 'report.html', context)

            # Handle Export action for issue/return
            if action == 'export':
                return export_books_csv(books, start_date, end_date, transacType)

            # Normal Filter action
            context = {
                'books': books,
                'start_date': start_date,
                'end_date': end_date,
                'type': transacType
            }
            return render(request, 'report.html', context)

        else:
            messages.error(request, 'All fields are required')
            return redirect('report')

    return render(request, 'report.html')


# CSV Export Functions 👇

def export_books_csv(books, start_date, end_date, transacType):
    response = HttpResponse(content_type='text/csv')
    filename = f"{transacType}_report_{start_date}_to_{end_date}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['User', 'Book Accession No', f'{transacType.title()} Date'])

    for book in books:
        writer.writerow([
            str(book.user),  # Adjust if you want user.name
            book.book.accession_no,
            book.date.strftime('%Y-%m-%d %H:%M')
        ])

    return response


def export_late_returns_csv(late_returns, start_date, end_date):
    response = HttpResponse(content_type='text/csv')
    filename = f"late_return_report_{start_date}_to_{end_date}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Student', 'Book Accession No', 'Return Date', 'Due Date', 'Days Late'])

    for item in late_returns:
        writer.writerow([
            str(item['user']),  # Adjust if you want item['user'].name
            item['book'].accession_no,
            item['return_date'].strftime('%Y-%m-%d'),
            item['due_date'].strftime('%Y-%m-%d'),
            item['days_late']
        ])

    return response

def download_sample(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_users.csv"'

    writer = csv.writer(response)

    # Sample header for Students
    writer.writerow(['Name', 'Roll No', 'Class ID', 'Section'])
    writer.writerow(['John Doe', '23CS101', 'CS101', 'A'])
    writer.writerow(['Jane Smith', '23CS102', 'CS101', 'B'])

    writer.writerow([])  # Empty row

    # Sample header for Teachers
    writer.writerow(['Name', 'Teacher ID', 'Department'])
    writer.writerow(['Dr. Kumar', 'TCH001', 'Physics'])
    writer.writerow(['Mrs. Rao', 'TCH002', 'Mathematics'])

    return response


def download_book_sample(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_books.csv"'

    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Accession Number','Title', 'Author', 'ISBN', 'Publisher', 'Year', 'Category'])
    
    # Write sample data rows
    writer.writerow(['EEC23001','The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'Scribner', '1925', 'Fiction'])
    writer.writerow(['EEC24001','To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'J.B. Lippincott & Co.', '1960', 'Fiction'])

    return response

def get_issued_user(request):
    book_id = request.GET.get('book_id')
    try:
        accession = Accession_No.objects.get(accession_no=book_id)
        issued_record = IssuedBooks.objects.get(book=accession, book__accession_no=book_id)

        user_object = issued_record.user  # ✅ This is correct now
        user_model_name = user_object._meta.model_name  # safer way

        if user_model_name == 'students':
            user_id = user_object.roll_no
            user_type = 'Student'
        elif user_model_name == 'teacher':
            user_id = user_object.teacher_id
            user_type = 'Teacher'
        else:
            return JsonResponse({'success': False, 'message': f'Issued user model not recognized. Got: {user_model_name}'})

        return JsonResponse({
            'success': True,
            'user_id': user_id,
            'user_type': user_type,
            'name': user_object.name
        })

    except IssuedBooks.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Book is not currently issued to any user.'})
    except Accession_No.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid accession number.'})
    
def ajaxSearchUser(request):
    if request.method == 'GET':
        uid = request.GET.get('user_id', '')
        if Students.objects.filter(
            Q(roll_no__icontains=uid)
        ).first():
            user = Students.objects.filter(
                Q(roll_no__icontains=uid)
            ).first()
            data = {
                'role': 'student',
                'name': user.name,
                'roll_no': user.roll_no,
                'class': user.class_id,
                'section': user.section,
                'issued_books': user.books_issued,
                'returned_books': user.books_returned,
                'pending_books': user.books_pending,
                'fine': user.fine
            }
            return JsonResponse({'status': 'success', 'user': data})

        elif Teacher.objects.filter(
            Q(teacher_id__icontains=uid)
        ).first():
            user = Teacher.objects.filter(
                Q(teacher_id__icontains=uid)
            ).first()
            data = {
                'role': 'teacher',
                'name': user.name,
                'teacher_id': user.teacher_id,
                'department': user.department,
                'issued_books': user.books_issued,
                'returned_books': user.books_returned,
                'pending_books': user.books_pending,
                'fine': user.fine
            }
            return JsonResponse({'status': 'success', 'user': data})

        return JsonResponse({'status': 'not_found'})
