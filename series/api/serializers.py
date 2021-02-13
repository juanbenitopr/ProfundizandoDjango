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

    def create(self, **kwargs) -> Serie:
        serie = Serie.objects.create(**self.validated_data)
        return serie

    def update(self, **kwargs) -> Serie:
        for attr, value in self.validated_data.items():
            setattr(self.instance, attr, value)

        self.instance.save()
        return self.instance

    def save(self, **kwargs):
        if self.instance is not None:
            self.instance = self.update()
        else:
            self.instance = self.create()

        return self.instance

