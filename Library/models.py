from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class Staff(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name="library_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="library_user_permissions", blank=True)
    def __str__(self):
        return self.username
