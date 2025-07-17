from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/parking_updates/$', consumers.ParkingConsumer.as_asgi()),
]