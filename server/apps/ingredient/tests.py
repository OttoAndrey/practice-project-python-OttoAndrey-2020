from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.ingredient.models import Ingredient


class NumPairAPITests(APITestCase):
    def setUp(self):
        self.test_instance_user = {'username': 'TestUsername', 'password': 'pass123'}
        url_user = reverse("users-list")
        response_user = self.client.post(url_user, self.test_instance_user, format='json', )

        self.token = 'Token ' + response_user.data['token']

        Ingredient.objects.create(name='Test ingredient', calorie=100)
        Ingredient.objects.create(name='Test ingredient new', calorie=100)

        self.test_instance_ingredient = {'name': 'Test ingredient fresh',
                                         'calorie': '100',
                                         }

        self.count_before = Ingredient.objects.count()

    def test_create_action_correct_instance(self):
        """
        Test POST ингредиент может создать только пользователь с токеном
        """
        url = reverse("ingredient-list")
        response = self.client.post(url, self.test_instance_ingredient, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_action_incorrect_instance(self):
        """
        Test POST ингредиент без токена создать нельзя
        """
        url = reverse("ingredient-list")
        response = self.client.post(url, self.test_instance_ingredient, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_action(self):
        """
        Test GET возвращает список всех ингредиентов
        """
        url = reverse('ingredient-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.count_before)

    def test_retrieve_action(self):
        """
        Test GET возвращает ингредиент по его id
        """
        obj = Ingredient.objects.first()

        url = reverse('ingredient-detail', args=(obj.id,))
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], obj.name)
        self.assertEqual(response.data['calorie'], obj.calorie)

    def test_retrieve_wrong_id_action(self):
        """
        Test GET при обращении к ингредиенту, которого не существует, вернет 404
        """
        obj = Ingredient.objects.order_by('id').last()

        url = reverse('ingredient-detail', args=(obj.id + 1,))
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_action(self):
        """
        Test PUT, PATCH не разрешены для ингредиента даже пользователям с токеном
        """
        obj = Ingredient.objects.first()

        url = reverse('ingredient-detail', args=(obj.id, ))
        response = self.client.put(url, self.test_instance_ingredient, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_action(self):
        """
        Test DELETE не разрешен для ингредиента даже пользователям с токеном
        """
        obj = Ingredient.objects.first()

        url = reverse('ingredient-detail', args=(obj.id, ))
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
