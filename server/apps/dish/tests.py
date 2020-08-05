from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.dish.models import Dish
from apps.ingredient.models import Ingredient


class DishSignalTests(TestCase):
    def test_sum_of_calories_is_calculated(self):
        """
        Test поле sum_of_calories было посчитано при создании блюда
        """
        self.test_instance_user = {'username': 'TestUsername', 'password': 'pass123'}
        url_user = reverse("users-list")
        response_user = self.client.post(url_user, self.test_instance_user, format='json', )

        self.token = 'Token ' + response_user.data['token']

        ingredient_first = Ingredient.objects.get(id=1)
        ingredient_second = Ingredient.objects.get(id=2)

        sum_of_calories = sum([ingredient_first.calorie, ingredient_second.calorie])

        count_before_catering = Dish.objects.count()
        self.test_instance_dish = {'name': 'Test dish first',
                                   'price': 100,
                                   'ingredients': ('1', '2'),
                                   }
        url_dish = reverse("dish-list")
        response_dish = self.client.post(url_dish, self.test_instance_dish, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response_dish.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), count_before_catering + 1)
        self.assertEqual(self.test_instance_dish['name'], response_dish.data['name'])
        self.assertEqual(sum_of_calories, float(response_dish.data['sum_of_calories']))


class NumPairAPITests(APITestCase):
    def setUp(self):
        self.test_instance_user = {'username': 'TestUsername', 'password': 'pass123'}
        url_user = reverse("users-list")
        response_user = self.client.post(url_user, self.test_instance_user, format='json', )

        self.token = 'Token ' + response_user.data['token']

        self.test_instance_dish = {'name': 'Test dish',
                                   'price': '100',
                                   'ingredients': ('1', '2'),
                                   }
        self.test_new_instance_dish = {'name': 'Test new dish',
                                       'price': '100',
                                       'ingredients': ('1', '2'),
                                       }
        url_dish = reverse("dish-list")
        self.client.post(url_dish, self.test_instance_dish, format='json', HTTP_AUTHORIZATION=self.token)
        self.client.post(url_dish, self.test_instance_dish, format='json', HTTP_AUTHORIZATION=self.token)

        self.count_before = Dish.objects.count()

    def test_create_action_correct_instance(self):
        """
        Test POST блюдо может создать только пользователь с токеном
        """
        url = reverse("dish-list")
        response = self.client.post(url, self.test_instance_dish, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_action_incorrect_instance(self):
        """
        Test POST блюдо без токена создать нельзя
        """
        url = reverse("dish-list")
        response = self.client.post(url, self.test_instance_dish, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_action(self):
        """
        Test GET возвращает список всех блюд
        """
        url = reverse('dish-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.count_before)

    def test_retrieve_action(self):
        """
        Test GET возвращает блюдо по его id
        """
        obj = Dish.objects.first()

        url = reverse('dish-detail', args=(obj.id,))
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], obj.name)
        self.assertEqual(response.data['price'], obj.price)
        self.assertEqual(response.data['sum_of_calories'], float(obj.sum_of_calories))
        self.assertEqual(response.data['ingredients'], list(obj.ingredients.values_list('id', flat=True)))
        self.assertEqual(response.data['owner'], obj.owner.id)

    def test_retrieve_wrong_id_action(self):
        """
        Test GET при обращении к блюдо, которого не существует, вернет 404
        """
        obj = Dish.objects.order_by('id').last()

        url = reverse('dish-detail', args=(obj.id + 1,))
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_action(self):
        """
        Test PUT изменять блюдо может только его владелец
        """
        obj = Dish.objects.last()

        url = reverse('dish-detail', args=(obj.id,))
        response = self.client.put(url, self.test_new_instance_dish, format='json', HTTP_AUTHORIZATION=self.token)

        obj = Dish.objects.last()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.name, response.data['name'])

    def test_update_without_token(self):
        """
        Test PUT изменить блюдо без токена не получится
        """
        obj = Dish.objects.last()

        url = reverse('dish-detail', args=(obj.id,))
        response = self.client.put(url, self.test_new_instance_dish, format='json', )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_action(self):
        """
        Test DELETE удалить блюдо может только владелец
        """
        obj = Dish.objects.first()

        url = reverse('dish-detail', args=(obj.id,))
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_without_token(self):
        """
        Test DELETE удалить блюдо без токена не получится
        """
        obj = Dish.objects.first()

        url = reverse('dish-detail', args=(obj.id,))
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
