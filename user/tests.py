from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser@mail.ru',
                                             email='testuser@mail.ru',
                                             password='testpass224')
        self.url = "http://localhost:8003/auth/jwt/create/"
        self.data = {'username': 'testuser@mail.ru', 'email': 'testuser@mail.ru', 'password': 'testpass224'}

    def test_token_auth(self):
        # Test token authentication
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        # Test token refresh
        response = self.client.post(reverse('token_refresh'), {'refresh': 'invalid-token'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(self.url, self.data)
        refresh_token = response.data['refresh']
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_register(self):
        # Test user registration
        data = {'username': 'newuser', 'password': 'newpass'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, 'newuser')

    def test_user_login(self):
        # Test user login
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_logout(self):
        # Test user logout
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_password_change(self):
        # Test user password change
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('password_change'), {'new_password': 'newpass'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass'))


