from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from classroom.serializers import ClassroomSerializer


class CreateClassroom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
