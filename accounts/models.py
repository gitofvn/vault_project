from django.db import models
from django.contrib.auth.models import User

class UserKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="encryption_key")
    encrypted_key = models.CharField(max_length=200)

    def __str__(self):
        return f"Encryption key for {self.user.username}"
