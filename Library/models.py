from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class Students(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=10)
    class_id = models.CharField(max_length=10)
    section =  models.CharField(max_length=10)
    def _str_(self):
        return self.name
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    def _str_(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100)
    def _str_(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    edition = models.CharField(max_length=50,blank=True,null=True)
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name='books')
    STATUS_CHOICES = [("Available", "Available"), ("Issued", "Issued"), ("Reserved", "Reserved")]
    availability_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Available")
    isbn = models.CharField(max_length=20, blank=True, null=True)
    def _str_(self):
        return self.title
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(Students, on_delete=models.CASCADE) 
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    expiry_date = models.DateField()


    def _str_(self):
        return f"{self.book.title} reserved by {self.user.username}"

class IssueBooks(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} issued to {self.student.user.get_full_name()}"
