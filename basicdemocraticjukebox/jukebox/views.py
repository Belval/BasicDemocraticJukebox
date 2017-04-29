import json
import uuid

from django.shortcuts import render, get_object_or_404
from django.views.static import serve
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Sum, Case, When, IntegerField, Count
from .models import Song, Vote


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
        s = Song.objects.create(title=f, uuid=uuid.uuid4())
        with open('./jukebox/songs/{}'.format(s.uuid), 'wb+') as out:
            out.write(request.FILES[f].read())
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
    return 