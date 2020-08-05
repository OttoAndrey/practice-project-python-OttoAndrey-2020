from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class NumPairAPITests(APITestCase):
    def setUp(self):
        User.objects.create(username='first obj', password='pass123')
        User.objects.create(username='second obj', password='pass123')

        self.count_before = User.objects.count()

        self.test_instance = {'username': 'TestUsername', 'password': 'pass123'}

    def test_create_action_correct_instance(self):
        """
        Test POST возвращает токен пользователя
        """
        url = reverse('users-list')
        response = self.client.post(url, self.test_instance, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.count_before + 1)

        self.assertEqual(self.test_instance['username'], response.data['username'])
        self.assertEqual(type(response.data['token']), str)
        self.assertEqual(Token.objects.last().key, response.data['token'])

    def test_list_action(self):
        """
        Test GET доступ к списку всех пользователей запрещен
        """
        url = reverse('users-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
