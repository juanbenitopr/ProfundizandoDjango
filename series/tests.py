import json
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from rest_framework import status

from series.models import Serie, Episode, Score


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
        self.assertIn('score', response_json)

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

    def test_set_score(self):
        user: User = User.objects.first()
        serie = Serie.objects.first()

        user.is_superuser = True
        user.save()

        self.client.force_login(user)

        response = self.client.put(f'/api/series/{serie.pk}/set-score/', data={'score': 4}, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        score = Score.objects.filter(serie_id=serie.pk).first()

        score.refresh_from_db()
        self.assertIsNotNone(score)
        self.assertEqual(score.score, 4)
        self.assertEqual(score.serie_id, serie.pk)
        self.assertEqual(score.user_id, user.pk)


class TestEpisode(TestCase):
    fixtures = ['series', 'users']

    def test_retrieve_episode(self):
        episode = Episode.objects.first()

        response = self.client.get(f'/api/episodes/{episode.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()

        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('id'), int)
        self.assertIsInstance(response_json.get('name'), str)
        self.assertIsInstance(response_json.get('number'), int)
        self.assertIn('score', response_json)

    def test_create_episode(self):
        user = User.objects.first()

        self.client.force_login(user)
        episode_dict = {'name': f'mock episode {uuid4()}', 'number': 1, 'serie': 1}

        response = self.client.post(f'/api/episodes/', episode_dict)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()
        self.assertIsInstance(response_json.get('id'), int)
        self.assertTrue(response_json.get('name'), episode_dict.get('name'))
        self.assertTrue(response_json.get('number'), episode_dict.get('number'))

    def test_create_episode_without_permission(self):
        episode_dict = {'name': f'mock episode {uuid4()}', 'number': 1, 'serie': 1}

        response = self.client.post(f'/api/episodes/', episode_dict)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
