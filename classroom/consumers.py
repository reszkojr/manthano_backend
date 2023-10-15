import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChannelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f'{self.scope}')
        await self.accept()

    async def disconnect(self, close_code):
        print(f'{self.scope["user"]} disconnected')
        pass

    async def receive(self, data):
        print(data)
