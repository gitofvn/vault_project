from django.db import models
from django.contrib.auth.models import User


class Credential(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='credentials'
    )
    site_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    site_url = models.URLField(blank=True, null=True) 
    other = models.TextField(blank=True, null=True)
    password_encrypted = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.site_name} ({self.username})"


