import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from series.api.serializers import SerieSerializer, DetailSerieSerializer, ScoreSerializer, EpisodeSerializer, \
    ScoreEpisodeSerializer
from series.models import Serie, Episode


class SeriesViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SerieSerializer
    queryset = Serie.objects.all()

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        super().__init__(**kwargs)

    def get_serializer_class(self):
        self.logger.error(self.action)
        if self.action == 'retrieve':
            return DetailSerieSerializer
        if self.action == 'set_score':
            return ScoreSerializer
        else:
            return self.serializer_class

    @action(detail=True, methods=['PUT'], url_path='set-score', permission_classes=[IsAdminUser])
    def set_score(self, request, pk: int):
        data = {'serie': pk, 'user': request.user.pk, 'score': int(request.data.get('score'))}

        serializer = self.get_serializer_class()(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status=status.HTTP_200_OK)


class EpisodeViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all()

    def get_serializer_class(self):
        if self.action == 'set_score':
            return ScoreEpisodeSerializer
        else:
            return self.serializer_class

    @action(detail=True, methods=['PUT'], url_path='set-score', permission_classes=[IsAdminUser])
    def set_score(self, request, pk: int):
        data = {'episode': pk, 'user': request.user.pk, 'score': int(request.POST['score'])}

        serializer = self.get_serializer_class()(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
