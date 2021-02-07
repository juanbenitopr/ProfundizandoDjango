from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from rest_framework import status

from series.models import Serie


class TestSeries(TestCase):
    fixtures = ['series', 'users']

    def test_retrieve_serie(self):
        serie = Serie.objects.first()

        response = self.client.get(f'/api/series/{serie.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()

        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('id'), int)
        self.assertIsInstance(response_json.get('title'), str)
        self.assertIsInstance(response_json.get('description'), str)
        self.assertIsInstance(response_json.get('episodes'), list)

        self.assertEqual(len(response_json.get('episodes')), serie.episode_set.all().count())

    def test_create_serie(self):
        user = User.objects.first()

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

