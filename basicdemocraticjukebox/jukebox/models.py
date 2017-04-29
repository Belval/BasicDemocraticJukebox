from django.db import models
from django.contrib.sessions.models import Session

class Song(models.Model):
    title = models.CharField(max_length=60)
    uuid = models.CharField(max_length=40)

class Vote(models.Model):
    song = models.ForeignKey('song', related_name='votes')
    session_key = models.CharField(max_length=128)
    is_positive = models.BooleanField(default=True) 

