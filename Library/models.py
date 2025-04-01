from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class Students(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=10)
    class_id = models.CharField(max_length=10)
    section =  models.CharField(max_length=10)
    books_issued = models.IntegerField(default=0)
    books_returned = models.IntegerField(default=0)
    books_pending = models.IntegerField(default=0)
    def __str__(self):
        return self.name
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    books_issued = models.IntegerField(default=0)
    books_returned = models.IntegerField(default=0)
    books_pending = models.IntegerField(default=0)
    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='books')
    availability_status = models.CharField(max_length=10, default="Available")
    isbn = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.title
class IssuedBooks(models.Model):
    user = models.ForeignKey(Students, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    def __str__(self):
        return f"{self.book.title} issued to {self.user.username}"
class ReturnedBooks(models.Model):
    user = models.ForeignKey(Students, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    return_date = models.DateField()
    condition = models.CharField(max_length=10, default="Good")
    def __str__(self):
        return f"{self.book.title} returned by {self.user.username}"