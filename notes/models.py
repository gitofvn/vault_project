from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Note(models.Model):
    user = models.ForeignKey(
        UserModel, 
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=100
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
