from rest_framework.routers import DefaultRouter

from series.api.views import SeriesViewset

router = DefaultRouter()

router.register(prefix='series', basename='series', viewset=SeriesViewset)