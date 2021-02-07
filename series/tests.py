from uuid import uuid4

from django.test import TestCase

# Create your tests here.
from series.models import Serie, Episode


class TestSeries(TestCase):

    def _generate_serie(self) -> Serie:
        serie = Serie.objects.create(title=f'mock serie {uuid4()}', description=f'mock description')

        for i in range(1, 6):
            Episode.objects.create(serie_id=serie.pk, name=f'mock episode {uuid4()}', number=i+1)

        return serie

    def test_retrieve_serie(self):
        serie = self._generate_serie()

        response = self.client.get(f'/api/series/{serie.id}/')

        response_json = response.json()

        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('id'), int)
        self.assertIsInstance(response_json.get('title'), str)
        self.assertIsInstance(response_json.get('description'), str)
        self.assertIsInstance(response_json.get('episodes'), list)

        self.assertEqual(len(response_json.get('episodes')), 5)

