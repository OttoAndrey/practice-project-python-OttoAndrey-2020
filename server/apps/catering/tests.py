from django.db.models import Avg
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catering.models import Catering
from apps.dish.models import Dish


class CateringSignalTests(TestCase):
    def test_avg_cost_is_calculated(self):
        """
        Test поле avg_cost было посчитано при создании заведения
        """
        self.test_instance_user = {'username': 'TestUsername', 'password': 'pass123'}
        url_user = reverse("users-list")
        response_user = self.client.post(url_user, self.test_instance_user, format='json', )

        self.token = 'Token ' + response_user.data['token']

        self.test_instance_dish_first = {'name': 'Test dish first',
                                         'price': 100,
                                         'ingredients': ('1', '2'),
                                         }
        self.test_instance_dish_second = {'name': 'Test dish second',
                                          'price': 300,
                                          'ingredients': ('1', '2'),
                                          }
        url_dish = reverse("dish-list")
        self.client.post(url_dish, self.test_instance_dish_first, format='json', HTTP_AUTHORIZATION=self.token)
        self.client.post(url_dish, self.test_instance_dish_second, format='json', HTTP_AUTHORIZATION=self.token)

        avg_cost = Dish.objects.all().aggregate(Avg('price'))['price__avg']
        print(avg_cost)

        count_before_catering = Catering.objects.count()
        self.test_instance_catering = {'name': 'Test catering',
                                       'open_time': '9:00',
                                       'close_time': '23:00',
                                       'address': 'Красноярск Мира 1',
                                       'dishes': ('1', '2'),
                                       }
        url_catering = reverse("catering-list")
        response_catering = self.client.post(url_catering, self.test_instance_catering, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response_catering.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Catering.objects.count(), count_before_catering + 1)
        self.assertEqual(self.test_instance_catering['name'], response_catering.data['name'])
        self.assertEqual(avg_cost, float(response_catering.data['avg_cost']))


class NumPairAPITests(APITestCase):
    def setUp(self):
        self.test_instance_user = {'username': 'TestUsername', 'password': 'pass123'}
        url_user = reverse("users-list")
        response_user = self.client.post(url_user, self.test_instance_user, format='json', )

        self.token = 'Token ' + response_user.data['token']

        self.test_instance_catering = {'name': 'Test catering',
                                       'open_time': '9:00',
                                       'close_time': '23:00',
                                       'address': 'Красноярск Мира 1',
                                       }
        self.test_new_instance_catering = {'name': 'Test new catering',
                                           'open_time': '12:00',
                                           'close_time': '01:00',
                                           'address': 'Красноярск Ленина 100',
                                           }
        url_catering = reverse("catering-list")
        self.client.post(url_catering, self.test_instance_catering, format='json', HTTP_AUTHORIZATION=self.token)
        self.client.post(url_catering, self.test_instance_catering, format='json', HTTP_AUTHORIZATION=self.token)

        self.count_before = Catering.objects.count()

    def test_create_action_correct_instance(self):
        """
        Test POST заведение может создать только пользователь с токеном
        """
        url = reverse("catering-list")
        response = self.client.post(url, self.test_instance_catering, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_action_incorrect_instance(self):
        """
        Test POST заведение без токена создать нельзя
        """
        url = reverse("catering-list")
        response = self.client.post(url, self.test_instance_catering, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_action(self):
        """
        Test GET возвращает список всех заведений
        """
        url = reverse('catering-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.count_before)

    def test_retrieve_action(self):
        """
        Test GET возвращает заведение по его id
        """
        obj = Catering.objects.first()

        url = reverse('catering-detail', args=(obj.id,))
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], obj.name)
        self.assertEqual(response.data['open_time'], str(obj.open_time))
        self.assertEqual(response.data['close_time'], str(obj.close_time))
        self.assertEqual(response.data['address'], obj.address)
        self.assertEqual(response.data['longitude'], str(obj.longitude))
        self.assertEqual(response.data['latitude'], str(obj.latitude))
        self.assertEqual(response.data['avg_cost'], obj.avg_cost)
        self.assertEqual(response.data['owner'], obj.owner.id)

    def test_retrieve_wrong_id_action(self):
        """
        Test GET при обращении к заведению, которого не существует, вернет 404
        """
        obj = Catering.objects.order_by('id').last()

        url = reverse('catering-detail', args=(obj.id + 1,))
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_action(self):
        """
        Test PUT изменять заведение может только его владелец
        """
        obj = Catering.objects.last()

        url = reverse('catering-detail', args=(obj.id,))
        response = self.client.put(url, self.test_new_instance_catering, format='json', HTTP_AUTHORIZATION=self.token)

        obj = Catering.objects.last()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.name, response.data['name'])

    def test_update_without_token(self):
        """
        Test PUT изменить заведение без токена не получится
        """
        obj = Catering.objects.last()

        url = reverse('catering-detail', args=(obj.id,))
        response = self.client.put(url, self.test_new_instance_catering, format='json', )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_action(self):
        """
        Test DELETE удалить заведение может только владелец
        """
        obj = Catering.objects.first()

        url = reverse('catering-detail', args=(obj.id,))
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_without_token(self):
        """
        Test DELETE удалить заведение без токена не получится
        """
        obj = Catering.objects.first()

        url = reverse('catering-detail', args=(obj.id,))
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
