from cryptography.fernet import Fernet
from django.conf import settings
from accounts.models import UserKey
import base64


def get_master_key():
    return settings.MASTER_KEY.encode()


def generate_user_key():
    return Fernet.generate_key()


def encrypt_user_key(user_key: bytes, master_key: bytes) -> str:
    fernet = Fernet(master_key)
    return fernet.encrypt(user_key).decode()


def decrypt_user_key(encrypted_user_key: str, master_key: bytes) -> bytes:
    fernet = Fernet(master_key)
    return fernet.decrypt(encrypted_user_key.encode())


def get_user_fernet(user):
    encrypted_key = user.encryption_key.encrypted_key
    master_key = get_master_key()

    user_key = decrypt_user_key(encrypted_key, master_key)

    return Fernet(user_key)


def encrypt_password(user, plaintext_password: str) -> str:
    """
    Encrypts a password (or note content) for a given user.
    """
    fernet = get_user_fernet(user)
    return fernet.encrypt(plaintext_password.encode()).decode()


def decrypt_password(user, encrypted_password: str) -> str:
    """
    Decrypts a password (or note content) for a given user.
    """
    fernet = get_user_fernet(user)
    return fernet.decrypt(encrypted_password.encode()).decode()
