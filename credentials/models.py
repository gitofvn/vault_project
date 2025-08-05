from django.db import models
from django.contrib.auth import get_user_model

from credentials.validators import validate_phone_number


UserModel = get_user_model()


class Category(models.Model):
    user = models.ForeignKey(
        UserModel, 
        on_delete=models.CASCADE, 
        related_name='categories'
    )

    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class Credential(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='credentials'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
    )
    site_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_phone_number]
    )
    site_url = models.CharField(max_length=255, blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    password_encrypted = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.site_name} ({self.username})"

    

