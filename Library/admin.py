from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import *
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "is_active")  # Customize fields displayed in admin
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_student',)}),  # Add is_student field
    )

    # Add 'is_student' when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('is_student',)}),  # Add is_student field in add panel
    )
    # Ensure password is hashed when saving from the admin panel
    def save_model(self, request, obj, form, change):
        if not change or "password" in form.changed_data:
            obj.password = make_password(obj.password)  # Hash password before saving
        super().save_model(request, obj, form, change)

# Register the custom Users model with the admin panel
admin.site.register(Users, CustomUserAdmin)
admin.site.register(StudentExtra)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Reservation)