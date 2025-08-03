from django.test import TestCase
from django.contrib.auth import get_user_model
from credentials.forms import CredentialForm
from credentials.models import Credential, Category

UserModel = get_user_model()

class TestCredentialForm(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="Testpass123!"
        )

        self.category = Category.objects.create(user=self.user, name="Work")

        self.data = {
            'category': self.category.id,
            'site_name': 'Test',
            'username': 'Test',
            'email': 'test@test.com',
            'phone_number': '123456789',
            'site_url': 'test.com',
            'other': 'Test',
            'password': 'SecretPass123!'
        }

    def test__form_is_valid__expect_success(self):
        form = CredentialForm(data=self.data, user=self.user)
        self.assertTrue(form.is_valid())

    def test__form_valid_data__saves_encrypted_password(self):
        form = CredentialForm(data=self.data, user=self.user)
        self.assertTrue(form.is_valid())
        credential = form.save(user=self.user)
        self.assertNotEqual(credential.password_encrypted, self.data['password'])
        self.assertTrue(Credential.objects.filter(pk=credential.pk).exists())

    def test__password_field_hidden_by_default(self):
        form = CredentialForm(user=self.user)
        self.assertEqual(form.fields['password'].widget.__class__.__name__, 'PasswordInput')

    def test__password_field_visible_when_show_password_true(self):
        form = CredentialForm(user=self.user, show_password=True)
        self.assertEqual(form.fields['password'].widget.__class__.__name__, 'TextInput')
