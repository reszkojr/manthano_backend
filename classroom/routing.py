from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<classroom_code>\w+)/(?P<channel_name>.+)/$', consumers.ChannelConsumer.as_asgi())
]
