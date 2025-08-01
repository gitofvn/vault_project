from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from utils.encryption import generate_user_key, encrypt_user_key, get_master_key
from .models import UserKey

@receiver(post_save, sender=User)
def create_user_encryption_key(sender, instance, created, **kwargs):
    if created:
        # Generate new Fernet key for this user
        user_key = generate_user_key()

        # Encrypt the key with Master Key
        encrypted_key = encrypt_user_key(user_key, get_master_key())

        # Save encrypted key in UserKey model
        UserKey.objects.create(user=instance, encrypted_key=encrypted_key)
