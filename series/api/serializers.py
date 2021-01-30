from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from series.models import Serie


class SerieSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    id = serializers.IntegerField(read_only=True)

    def validate_title(self, title: str):
        series = Serie.objects.filter(title=title)
        if series.exists():
            raise ValidationError('The title already exists')
        return title

    def validate_description(self, description: str):
        if not description:
            raise ValidationError('The description cannot be blank')
        return description
