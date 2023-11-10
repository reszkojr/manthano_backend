from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import ManthanoUser
from classroom.models import Classroom

from classroom.serializers import ClassroomSerializer


class CreateClassroomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinClassroomView(APIView):
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


class GetUserClassroomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user: ManthanoUser = request.user
        if user.classroom is not None:
            return Response({'classroom_code': user.classroom.code}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetClassroomChannelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user: ManthanoUser = request.user
        response = {}
        for i in user.classroom.channels.all():
            response[i.id] = i.name
        if user.classroom is not None:
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
