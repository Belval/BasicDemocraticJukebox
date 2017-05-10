from django.db import models
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime


class Song(models.Model):
    title = models.CharField(max_length=60)
    uuid = models.CharField(max_length=40)
    length = models.IntegerField()

class Vote(models.Model):
    song = models.ForeignKey('song', related_name='votes')
    session_key = models.CharField(max_length=128)
    is_positive = models.BooleanField(default=True) 

class PlayedSong(models.Model):
    song = models.ForeignKey('song', related_name='play')
    start = models.DateTimeField(auto_now=True)

    def is_over(self):
        return self.start + datetime.timedelta(0, self.song.length) <= timezone.now() + datetime.timedelta(0, 5)