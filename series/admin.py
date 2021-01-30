from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin, register

from series.models import Serie, Episode


class SeriesAdmin(ModelAdmin):
    list_display = ('title', 'description')

admin.site.register(Serie, SeriesAdmin)

@register(Episode)
class EpisodeAdmin(ModelAdmin):
    pass