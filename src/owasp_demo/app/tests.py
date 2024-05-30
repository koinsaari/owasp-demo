from unittest.mock import patch

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


class SecurityFlawFixTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.testuser1 = User.objects.create_user(username='testuser1', password='password000')
        self.testuser1.save()
        Profile.objects.create(
            user=self.testuser1,
            email='testuser1@example.com',
            phone_number='12345',
            is_public=True
        )

        self.testuser2 = User.objects.create_user(username='testuser2', password='password123')
        self.testuser2.save()
        Profile.objects.create(
            user=self.testuser2,
            email='testuser2@example.com',
            phone_number='67890',
            is_public=False
        )

        self.testuser3 = User.objects.create_user(username='testuser3', password='password456')
        self.testuser3.save()
        Profile.objects.create(
            user=self.testuser3,
            email='testuser3@example.com',
            phone_number='54321',
            is_public=True
        )

    def test_register_password_not_stored_in_plain_text(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser4',
            'password': 'password789',
            'email': 'testuser4@example.com',
            'phone_number': '98765'
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='testuser4')
        self.assertNotEqual(new_user.password, 'password789')
        self.assertTrue(new_user.check_password('password789'))

    @patch('app.views.logger')
    def test_login_with_logging(self, mock_logger):
        response = self.client.post(reverse('login'), {
            'username': 'testuser1',
            'password': 'wrong123'
        })
        self.assertContains(response, "Invalid login. Please try again.")
        mock_logger.warning.assert_called_with("Invalid login attempt for user: testuser1")

    @patch('app.views.logger')
    def test_error_handling_does_not_reveal_stack_trace(self, mock_logger):
        with patch('app.views.authenticate', side_effect=Exception("Test exception")):
            response = self.client.post(reverse('login'), {
                'username': 'someuser',
                'password': 'somepassword123'
            })
            self.assertNotContains(response, "Traceback")
            self.assertContains(response, "An error has occurred. Please try again later.")
            mock_logger.error.assert_called_with("An error occurred during login: Test exception")

    def test_sql_injection_protected(self):
        self.client.login(username='testuser1', password='password000')
        response = self.client.get(reverse('search_users'), {'username': "' OR 1=1 --"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['users']), 0)

    def test_access_control_prevents_profile_view(self):
        self.client.login(username='testuser1', password='password000')
        response = self.client.get(reverse('user_profile', args=[self.testuser2.id]))
        self.assertEqual(response.status_code, 403)
