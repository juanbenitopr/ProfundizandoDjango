from django.db.models import Avg
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from series.models import Serie, Episode, Score, ScoreEpisode


class SerieSerializer(ModelSerializer):
    class Meta:
        model = Serie
        fields = ('id', 'title', 'description')


class EpisodeSerializer(ModelSerializer):
    score = SerializerMethodField()

    def get_score(self, episode: Episode) -> int:
        return ScoreEpisode.objects.filter(episode_id=episode.pk).aggregate(score=Avg('score')).get('score')

    class Meta:
        model = Episode
        fields = ('id', 'name', 'number', 'score', 'serie')


class DetailSerieSerializer(ModelSerializer):
    episodes = EpisodeSerializer(source='episode_set', many=True)
    score = SerializerMethodField(source='score')

    def get_score(self, serie: Serie) -> int:
        return Score.objects.filter(serie_id=serie.id).aggregate(score=Avg('score')).get('score')

    class Meta:
        model = Serie
        fields = ('id', 'title', 'description', 'episodes', 'score')


class ScoreSerializer(ModelSerializer):

    class Meta:
        model = Score
        fields = ('id', 'user', 'serie', 'score')


class ScoreEpisodeSerializer(ModelSerializer):

    class Meta:
        model = ScoreEpisode
        fields = ('id', 'episode', 'user', 'score')

