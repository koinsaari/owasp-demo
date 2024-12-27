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

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile
import random


class Command(BaseCommand):
    # Command to populate the database with dummy users.
    help = 'Populates the database with dummy users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of users to create')

    def handle(self, *args, **kwargs):
        num_users = kwargs['num_users']
        for i in range(num_users):
            username = f'user{i}'
            email = f'user{i}@example.com'
            password = f'password{i}{i}{i}'
            phone_number = f'123456789{i}'
            is_public = random.choice([True, False])
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            Profile.objects.create(
                user=user,
                email=email,
                phone_number=phone_number,
                password=password,
                is_public=is_public
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created user {username} with profile set to {is_public}'
                )
            )
