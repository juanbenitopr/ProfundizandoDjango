from rest_framework.routers import DefaultRouter

from series.api.views import SeriesViewset, EpisodeViewset

router = DefaultRouter()

router.register(prefix='series', basename='series', viewset=SeriesViewset)
router.register(prefix='episodes', basename='series', viewset=EpisodeViewset)
