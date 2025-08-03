from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class TestRegisterUserView(TestCase):

    def setUp(self):
        self.url = reverse('register-user')
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'ValidPass123!',
            'reenter_password': 'ValidPass123!',
        }


    def test__get_request__renders_register_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register-user.html')


    def test__creates_user_and_redirects_to_login_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user_exists = UserModel.objects.filter(email='newuser@example.com').exists()
        self.assertTrue(user_exists)


    def test__try_register_with_mismatched_passwords__shows_error(self):
        data = self.valid_data.copy()
        data['reenter_password'] = 'DifferentPass123!'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match.")


    def test__try_register_with_duplicate_email__shows_error(self):
        UserModel.objects.create_user(
            username="existinguser",
            email="newuser@example.com",
            password="TestPass123!"
        )

        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This email is already in use.")
