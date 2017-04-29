from django.conf.urls import url
from .views import index, get_songs, upload, upvote, downvote

urlpatterns = [
    url(r'^$', index),
    url(r'^songs/$', get_songs),
    url(r'^upload/$', upload),
    url(r'^upvote/(\d+)/$', upvote),
    url(r'^downvote/(\d+)/$', downvote),
]