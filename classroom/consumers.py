from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

import json

from classroom.models import *


class ChannelConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def check_user_classroom(self, user, classroom):
        return user.classroom != classroom

    async def connect(self):
        classroom_code = self.scope["url_route"]["kwargs"]["classroom_code"]
        channel_name = self.scope["url_route"]["kwargs"]["channel_name"]
        self.group_name = classroom_code

        try:
            classroom = await database_sync_to_async(Classroom.objects.get)(code=classroom_code,)
            print("classroom: %s" % classroom)
        except:
            return await self.close()

        try:
            channel = await database_sync_to_async(Channel.objects.get)(name=channel_name, classroom=classroom)
            print("channel: %s" % channel)
        except:
            return await self.close()

        if await self.check_user_classroom(self.scope['user'], classroom):
            return await self.close()

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        user = self.scope["user"]
        msg = text_data_json["message"]

        data = {
            "type": 'chat_message',
            "user": user.username,
            "user_id": user.id,
            "avatar": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnIKokCKPGuGwDDP1oqr80tYlIzdxTmxh8CQ&usqp=CAU',
            "message": msg,
        }

        await self.channel_layer.group_send(
            self.group_name,
            data
        )

    async def chat_message(self, event):
        response = {
            'type': 'websocket.send',
            'user': event['user'],
            'message': event['message']
        }
        await self.send(json.dumps(event))
