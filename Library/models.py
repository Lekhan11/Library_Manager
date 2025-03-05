from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class Users(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name="library_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="library_user_permissions", blank=True)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "User"  
        verbose_name_plural = "Users" 
class StudentExtra(models.Model):
    user = models.OneToOneField(Users,on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    class_name = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    def __str__(self):
        return self.roll_no
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
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
    def __str__(self):
        return self.title
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE) 
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    expiry_date = models.DateField()


    def __str__(self):
        return f"{self.book.title} reserved by {self.user.username}"

