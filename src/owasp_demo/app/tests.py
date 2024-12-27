# Copyright (c) 2024 Aaro Koinsaari
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from unittest.mock import patch

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


class SecurityFlawTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.testuser1 = User.objects.create_user(username='testuser1', password='password000')
        self.testuser1.save()
        Profile.objects.create(
            user=self.testuser1,
            email='testuser1@example.com',
            phone_number='12345',
            password='password000'
        )

        self.testuser2 = User.objects.create_user(username='testuser2', password='password123')
        self.testuser2.save()
        Profile.objects.create(
            user=self.testuser2,
            email='testuser2@example.com',
            phone_number='67890',
            password='password123'
        )

        self.testuser3 = User.objects.create_user(username='testuser3', password='password456')
        self.testuser3.save()
        Profile.objects.create(
            user=self.testuser3,
            email='testuser3@example.com',
            phone_number='54321',
            password='password456'
        )

    def test_register_password_stored_in_plain_text(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser4',
            'password': 'password789',
            'email': 'testuser4@example.com',
            'phone_number': '98765'
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='testuser4')
        self.assertEqual(new_user.profile.password, 'password789')

    @patch('app.views.logger')
    def test_login_no_logging(self, mock_logger):
        response = self.client.post(reverse('login'), {
            'username': 'testuser1',
            'password': 'wrong123'
        })
        self.assertContains(response, "Invalid login. Your username or password was wrong.")
        mock_logger.error.assert_not_called()

    def test_error_handling_reveals_stack_trace(self):
        response = self.client.post(reverse('login'), {
            'username': 'someuser',
            'password': 'somepassword123'
        })
        self.assertContains(response, "Error:")
        self.assertContains(response, "Traceback")

    def test_sql_injection(self):
        self.client.login(username='testuser1', password='password000')
        response = self.client.get(reverse('search_users'), {'username': "' OR 1=1 --"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['users']), 2)

    def test_broken_access_control(self):
        self.client.login(username='testuser1', password='password000')
        response = self.client.get(reverse('user_profile', args=[self.testuser2.id]))
        self.assertEqual(response.status_code, 200)
