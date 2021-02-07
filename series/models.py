from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import CASCADE


class Serie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title

class Episode(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=50)
    serie = models.ForeignKey(Serie, on_delete=CASCADE)

    def __str__(self):
        return f'{self.name} - {self.number}'

class Score(models.Model):
    serie = models.ForeignKey(Serie, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    score = models.IntegerField()

