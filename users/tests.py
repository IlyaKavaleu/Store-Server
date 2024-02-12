from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from users.forms import UserRegisterForm
from users.models import User, EmailVerification
from datetime import timedelta


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': '',
            'last_name': '',
            'username': 'ninjame',
            'email': 'kavaleuilia@gmail.com',
            'password1': 'Middleweightchampion1',
            'password2': 'Middleweightchampion1'
        }

    def test_user_register_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Registration')
        self.assertTemplateUsed(response, 'users/register.html')


    def test_user_register_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() > timedelta(hours=48)).date()
        )

    def test_user_register_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.', html=True)
