import json
from django.shortcuts import render

from rest_framework import status
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import ManthanoUser
from classroom.models import *

from classroom.serializers import *


class CreateClassroomView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinClassroomView(views.APIView):
    def post(self, request, format=None):
        classroom_code = request.data.get('classroom_code')
        try:
            classroom = Classroom.objects.get(code=classroom_code)
        except Classroom.DoesNotExist:
            return Response('Classroom not found.', status=status.HTTP_404_NOT_FOUND)

        user: ManthanoUser = request.user
        if user.classroom:
            return Response('Your Classroom is already defined.', status=status.HTTP_400_BAD_REQUEST)

        user.classroom = classroom
        user.save()

        return Response(f'User {user} joined classroom {classroom.name} successfully.')


class GetUserClassroomView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user: ManthanoUser = request.user
        if user.classroom is not None:
            serializer = ClassroomSerializer(user.classroom)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetClassroomChannelsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user: ManthanoUser = request.user
        response = {}
        for i in user.classroom.channels.all():
            response[i.id] = i.name
        if user.classroom is not None:
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetClassroomJitsiChannelsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user: ManthanoUser = request.user
        response = {}
        for i in user.classroom.jitsi_channels.all():
            response[i.id] = i.name
        if user.classroom is not None:
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetChannelMessagesView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        channel_name = request.query_params.get('channel_name')
        try:
            channel = Channel.objects.get(classroom=request.user.classroom, name=channel_name)
        except Channel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(channel__classroom=request.user.classroom, channel=channel)
        if messages.count() == 0:
            return Response([], status=status.HTTP_200_OK)

        serializer = (MessageSerializer(messages, many=True))
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddChannelView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: ManthanoUser = request.user
        channel_name = request.data.get('channel_name')

        channel, created = Channel.objects.get_or_create(name=channel_name, classroom=user.classroom)
        if not created:
            response = {
                'error': {
                    'message': f'Channel with name "{channel.name}" already exists.'
                }
            }
            return Response(json.dumps(response), content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

        serializedChannel = ChannelSerializer(channel)

        return Response(serializedChannel.data, content_type='application/json', status=status.HTTP_201_CREATED)


class AddJitsiChannelView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: ManthanoUser = request.user
        channel_name = request.data.get('channel_name')

        channel, created = JitsiChannel.objects.get_or_create(
            name=channel_name, classroom=user.classroom, room_name=channel_name)
        if not created:
            response = {
                'error': {
                    'message': f'Channel with name "{channel.name}" already exists.'
                }
            }
            return Response(json.dumps(response), content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

        serializedChannel = JitsiChannelSerializer(channel)

        return Response(serializedChannel.data, content_type='application/json', status=status.HTTP_201_CREATED)


class UpdateChannelView(generics.UpdateAPIView):
    queryset = Channel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChannelSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        newChannel = json.loads(request.data.get('channel'))
        serializer = self.get_serializer(instance, data=newChannel, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateJitsiChannelView(generics.UpdateAPIView):
    queryset = JitsiChannel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = JitsiChannelSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        newChannel = json.loads(request.data.get('channel'))
        serializer = self.get_serializer(instance, data=newChannel, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteChannelView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user: ManthanoUser = request.user
        try:
            channel = Channel.objects.get(id=id).delete()
        except Channel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(json.dumps(channel), content_type='application/json', status=status.HTTP_201_CREATED)


class DeleteJitsiChannelView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user: ManthanoUser = request.user
        try:
            channel = JitsiChannel.objects.get(id=id).delete()
        except JitsiChannel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(json.dumps(channel), content_type='application/json', status=status.HTTP_201_CREATED)


class UpdateMessageView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        newMessage = json.loads(request.data.get('message'))
        newMessage['edited'] = True

        serializer = self.get_serializer(instance, data=newMessage, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteMessageView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user: ManthanoUser = request.user
        try:
            message = Message.objects.get(id=id).delete()
        except Channel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(json.dumps(message), content_type='application/json', status=status.HTTP_201_CREATED)
