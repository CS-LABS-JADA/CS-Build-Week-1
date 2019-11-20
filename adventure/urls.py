from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('create_rooms', api.create_rooms),
    url('get_rooms', api.get_rooms),
]