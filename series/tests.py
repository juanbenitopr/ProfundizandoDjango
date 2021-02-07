from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from rest_framework import status

from series.models import Serie, Episode


class TestSeries(TestCase):

    def _generate_user(self) -> User:
        user = User.objects.create(username=f'fake user {uuid4()}', password='supersegura',
                                   email=f'fake email {uuid4()}')

        return user

    def _generate_serie(self) -> Serie:
        serie = Serie.objects.create(title=f'mock serie {uuid4()}', description=f'mock description')

        for i in range(1, 6):
            Episode.objects.create(serie_id=serie.pk, name=f'mock episode {uuid4()}', number=i + 1)

        return serie

    def test_retrieve_serie(self):
        serie = self._generate_serie()

        response = self.client.get(f'/api/series/{serie.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()

        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('id'), int)
        self.assertIsInstance(response_json.get('title'), str)
        self.assertIsInstance(response_json.get('description'), str)
        self.assertIsInstance(response_json.get('episodes'), list)

        self.assertEqual(len(response_json.get('episodes')), 5)

    def test_create_serie(self):
        user = self._generate_user()

        self.client.force_login(user)
        serie_dict = {'title': f'mock serie {uuid4()}', 'description': f'description serie {uuid4()}'}

        response = self.client.post(f'/api/series/', serie_dict)

        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response_json.get('id'), int)
        self.assertTrue(response_json.get('title'), serie_dict.get('title'))
        self.assertTrue(response_json.get('description'), serie_dict.get('description'))

    def test_create_serie_without_permission(self):
        serie_dict = {'title': f'mock serie {uuid4()}', 'description': f'description serie {uuid4()}'}

        response = self.client.post(f'/api/series/', serie_dict)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

