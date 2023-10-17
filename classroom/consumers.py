import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChannelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print(f'{self.scope["user"]} disconnected')
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']

        await self.send(text_data=msg)
