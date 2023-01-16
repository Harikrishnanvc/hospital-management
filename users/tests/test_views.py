from django.test import TestCase
from django.urls import reverse
from users.models import LoginCredentials


class BaseTest(TestCase):
    def setUp(self):
        self.patient = 'register-patient'
        self.register_url = reverse('%s' % self.patient)
        self.login_url = reverse('login')
        self.user = {
            'credentials': 'patient02',
            'password': '1234',
        }

        self.user_unmatching_password = {

            'email': 'testemail@gmail.com',
            'credentials': 'test',
            'password': 'test',
            'password2': 'test',
            'first_name': 'test',
            'last_name': 'user'
        }

        self.user_invalid_email = {

            'email': 'test.com',
            'username': 'username',
            'password': 'teslatt',
            'password2': 'teslatto',
            'name': 'fullname'
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')
