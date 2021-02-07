from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from series.api.serializers import SerieSerializer, DetailSerieSerializer
from series.models import Serie


class SeriesViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SerieSerializer
    queryset = Serie.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailSerieSerializer
        else:
            return self.serializer_class
