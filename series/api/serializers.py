from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from series.models import Serie, Episode


class SerieSerializer(ModelSerializer):
    class Meta:
        model = Serie
        fields = ('id', 'title', 'description')


class EpisodeSerializer(ModelSerializer):

    class Meta:
        model = Episode
        fields = ('id', 'name')


class DetailSerieSerializer(ModelSerializer):
    episodes = EpisodeSerializer(source='episode_set', many=True)
    # episodes = SerializerMethodField()

    def get_episodes(self, instance: Serie):
        return list(instance.episode_set.values('id', 'name'))

    class Meta:
        model = Serie
        fields = ('id', 'title', 'description', 'episodes')

