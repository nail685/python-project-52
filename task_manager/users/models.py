from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    password1 = models.CharField(max_length=150)
    password2 = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password1", "password2"]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'