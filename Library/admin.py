from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import *
# Register the custom Users model with the admin panel
admin.site.register(Students)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Reservation)
admin.site.register(IssueBooks)
