from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from series.models import Serie, Episode, Score


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

    class Meta:
        model = Serie
        fields = ('id', 'title', 'description', 'episodes')


class ScoreSerializer(ModelSerializer):

    class Meta:
        model = Score
        fields = ('id', 'user', 'serie', 'score')

