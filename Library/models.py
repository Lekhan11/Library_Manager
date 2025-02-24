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

class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    issued = models.IntegerField(default=0)
    def __str__(self):
        return self.title