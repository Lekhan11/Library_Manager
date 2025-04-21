from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class Students(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=10)
    class_id = models.CharField(max_length=10)
    section =  models.CharField(max_length=10)
    books_issued = models.IntegerField(default=0)
    books_returned = models.IntegerField(default=0)
    books_pending = models.IntegerField(default=0)
    issued_books = GenericRelation('IssuedBooks', content_type_field='content_type', object_id_field='object_id')
    fine = models.IntegerField(default=0)
    def __str__(self):
        return self.roll_no
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    books_issued = models.IntegerField(default=0)
    books_returned = models.IntegerField(default=0)
    books_pending = models.IntegerField(default=0)
    fine = models.IntegerField(default=0)
    issued_books = GenericRelation('IssuedBooks', content_type_field='content_type', object_id_field='object_id')

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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
    object_id = models.PositiveIntegerField(null=True)
    user = GenericForeignKey('content_type', 'object_id')

    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.book.title} issued to {self.user}"
class ReturnedBooks(models.Model):
    # Content type and object ID fields for the user (could be a Student or Teacher)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
    object_id = models.PositiveIntegerField(null=True)
    user = GenericForeignKey('content_type', 'object_id')

    # Foreign key for the book
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    
    # Return date and condition of the book
    return_date = models.DateField()
    condition = models.CharField(max_length=10, default="Good")
    
    def __str__(self):
        return f"{self.book.title} returned by {self.user}"
class Setting(models.Model):
    maxDueStud = models.IntegerField(default=0)
    maxDueTeach = models.IntegerField(default=0)
    fineStud = models.IntegerField(default=0)
    fineTeach = models.IntegerField(default=0)
    logo = models.ImageField(upload_to='logo', blank=True, null=True)
    def __str__(self):
        return "Settings"
    
class Transaction(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
    object_id = models.PositiveIntegerField(null=True)
    user = GenericForeignKey('content_type', 'object_id')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('issue', 'Issue'), ('return', 'Return')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.book.title} by {self.user.username}"