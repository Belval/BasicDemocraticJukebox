from django.conf.urls import url
from .views import index, get_songs, get_song, upload, get_current_song, upvote, downvote

urlpatterns = [
    url(r'^$', index),
    url(r'^songs/$', get_songs),
    url(r'^upload/$', upload),
    url(r'^upvote/(\d+)/$', upvote),
    url(r'^downvote/(\d+)/$', downvote),
    url(r'^currentsong/$', get_current_song),
    url(r'^songdata/(\d+)/$', get_song),
]