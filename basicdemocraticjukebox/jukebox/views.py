import json
import uuid

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Song, Vote


def index(request):
    return render(request, 'jukebox/index.html', {})

def get_songs(request):
    songs = list(Song.objects.all())
    return HttpResponse(serializers.serialize('json', songs), status=200) 

@csrf_exempt
def upload(request):
    for f in request.FILES:
        s = Song.objects.create(title=f, uuid=uuid.uuid4())
        with open('./jukebox/songs/{}'.format(s.uuid), 'wb+') as out:
            out.write(request.FILES[f].read())
    return HttpResponse(status=200)

@csrf_exempt
def upvote(request, id):
    key = request.session.session_key
    song = get_object_or_404(Song, id)
    try:
        vote = song.votes.get(session_id=key)
        vote.is_positive = True
        vose.save()
    except:
        Vote.objects.create(song=song, session_id=key, is_positive=True)
    return HttpResponse(status=200)

@csrf_exempt
def downvote(request, id):
    key = request.session.session_key
    song = get_object_or_404(Song, id)
    try:
        vote = song.votes.get(session_id=key)
        vote.is_positive = False
        vose.save()
    except:
        Vote.objects.create(song=song, session_id=key, is_positive=False)
    return HttpResponse(status=200)