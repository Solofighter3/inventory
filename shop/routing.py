from django.urls import path
from . import consumers

websocket_urlpatternns=[
                path(r'ws/<int:room_name>/',consumers.Chatconsumer.as_asgi())
        ]