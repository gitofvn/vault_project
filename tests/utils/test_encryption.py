from django.test import TestCase
from django.contrib.auth import get_user_model
from utils import encryption

UserModel = get_user_model()

class TestEncryption(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Testpass123!"
        )
        self.user_key = self.user.encryption_key

    def test__get_master_key__returns_bytes(self):
        key = encryption.get_master_key()
        self.assertIsInstance(key, bytes)

    def test__generate_user_key__returns_bytes(self):
        key = encryption.generate_user_key()
        self.assertIsInstance(key, bytes)
        self.assertGreater(len(key), 0)

    def test__encrypt_and_decrypt_user_key__expect_original_value(self):
        original_key = encryption.generate_user_key()
        master_key = encryption.get_master_key()

        encrypted_key = encryption.encrypt_user_key(original_key, master_key)
        decrypted_key = encryption.decrypt_user_key(encrypted_key, master_key)

        self.assertEqual(original_key, decrypted_key)

