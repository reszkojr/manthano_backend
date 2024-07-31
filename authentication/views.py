import os
from rest_framework import views, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from pathlib import Path

from authentication.models import ManthanoUser, Professor, Student, Subject
from .jaasjwt import JaaSJwtBuilder
from . import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = ManthanoUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer


class UserInformation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


class FirstTimeLogin(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if (Student.objects.filter(user=request.user).exists() or Professor.objects.filter(user=request.user).exists()):
            return Response('A Student/Professor object already was created for this user', status=status.HTTP_404_NOT_FOUND)
        return Response('A Student/Professor object was not created for this user', status=status.HTTP_200_OK)


class UserSetup(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        if Student.objects.filter(user=user).exists() or Professor.objects.filter(user=user).exists():
            return Response('This user is already associated with a professor/student.', status=status.HTTP_409_CONFLICT)

        user.academic_email = data['academic_email']
        user.save()

        if data['role'] == 'student':
            student = Student.objects.create(
                user=user,
                enrollment=data['enrollment'],
            )
            return Response(f'Student {student} created', status=status.HTTP_201_CREATED)

        elif data['role'] == 'professor':
            professor = Professor.objects.create(
                user=user,
                academic_rank=data['academic_rank']
            )
            return Response(f'Professor {professor} created', status=status.HTTP_201_CREATED)

        return Response('Invalid role specified.', status=status.HTTP_400_BAD_REQUEST)


class RetrieveJaasToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from decouple import config

        try:
            BASE_DIR = Path(__file__).resolve().parent.parent
            fp = os.path.join(BASE_DIR, 'jitsi-key.pem')
            private_key = open(fp, 'r')
        except Exception as e:
            return Response('There was an error while reading Jitsi private API key.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = request.user

        jaasJWT = JaaSJwtBuilder()

        token = jaasJWT.withDefaults() \
            .withUserName(user.username) \
            .withUserEmail(user.email) \
            .withUserId(user.id) \
            .withApiKey(config('JITSI_API_KEY')) \
            .withAppID(config('JITSI_APP_ID')) \
            .signWith(private_key.read())

        return Response(token)
