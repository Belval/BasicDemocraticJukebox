import json
import uuid
import os

from mutagen.mp3 import MP3
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.views.static import serve
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Sum, Case, When, IntegerField, Count
from .models import Song, Vote, PlayedSong


def index(request):
    return render(request, 'jukebox/index.html', {})

def get_songs(request):
    songs = list(Song.objects.all().annotate(upvote=Sum(Case(
        When(votes__is_positive=True, then=1),
        default=0,
        output_field=IntegerField()
    )), downvote=Sum(Case(
        When(votes__is_positive=False, then=1),
        default=0,
        output_field=IntegerField()
    ))).order_by('-upvote').values())
    return HttpResponse(json.dumps(songs, cls=serializers.json.DjangoJSONEncoder), status=200) 

@csrf_exempt
def upload(request):
    for f in request.FILES:
        song_uuid = uuid.uuid4()
        with open('./jukebox/songs/{}'.format(song_uuid), 'wb+') as out:
            out.write(request.FILES[f].read())
        song_length = MP3('./jukebox/songs/{}'.format(song_uuid)).info.length
        print(song_length)
        s = Song.objects.create(title=f, uuid=song_uuid, length=song_length)
    return HttpResponse(status=200)

@csrf_exempt
def upvote(request, id):
    if not request.session.exists(request.session.session_key):
        request.session.create() 
    key = request.session.session_key
    song = get_object_or_404(Song, pk=id)
    try:
        vote = song.votes.get(session_key=key)
        vote.is_positive = True
        vote.save()
    except:
        Vote.objects.create(song=song, session_key=key, is_positive=True)
    return HttpResponse(status=200)

@csrf_exempt
def downvote(request, id):
    if not request.session.exists(request.session.session_key):
        request.session.create() 
    key = request.session.session_key
    song = get_object_or_404(Song, pk=id)
    try:
        vote = song.votes.get(session_key=key)
        vote.is_positive = False
        vote.save()
    except:
        Vote.objects.create(song=song, session_key=key, is_positive=False)
    return HttpResponse(status=200)

def get_current_song(request):
    try:
        current_song = PlayedSong.objects.all().order_by('-start')[0]
        if current_song.is_over():
            current_song.song.votes.all().delete()
            new_current_song = PlayedSong.objects.create(song=Song.objects.all().annotate(upvote=Sum(Case(When(votes__is_positive=True, then=1), default=0, output_field=IntegerField()))).order_by('-upvote')[0])
            song_dict = model_to_dict(new_current_song)
            song_dict['song_title'] = new_current_song.song.title
            return HttpResponse(json.dumps(song_dict), content_type='application/json')        
        else:
            song_dict = model_to_dict(current_song)
            song_dict['song_title'] = current_song.song.title
            return HttpResponse(json.dumps(song_dict), content_type='application/json')
    except Exception as e:
        current_song = PlayedSong.objects.create(song=Song.objects.all().annotate(upvote=Sum(Case(When(votes__is_positive=True, then=1), default=0, output_field=IntegerField()))).order_by('-upvote')[0])
        song_dict = model_to_dict(current_song)
        song_dict['song_title'] = current_song.song.title
        return HttpResponse(json.dumps(model_to_dict(current_song)), content_type='application/json')

def get_song(request, id):
    song = get_object_or_404(Song, pk=id)
    with open(os.path.join(settings.BASE_DIR, 'jukebox/songs', song.uuid), 'rb') as f:
        return HttpResponse(content=f.read(), content_type='audio/mpeg')