from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class UserKey(models.Model):
    user = models.OneToOneField(
        AppUser, 
        on_delete=models.CASCADE, 
        related_name="encryption_key"
    )
    encrypted_key = models.CharField(max_length=200)

    def __str__(self):
        return f"Encryption key for {self.user.username}"
