from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    user_type = models.CharField(max_length=10)
    age = models.IntegerField(null = True,default = 18)
    def __str__(self):
        return self.username
