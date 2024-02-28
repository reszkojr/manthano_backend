import os
from rest_framework import views, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from pathlib import Path

from authentication.models import ManthanoUser
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


class RetrieveJaasToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from decouple import config

        try:
            BASE_DIR = Path(__file__).resolve().parent.parent
            fp = os.path.join(BASE_DIR, 'jitsi-key.pem')
            private_key = open(fp, 'r')
        except Exception as e:
            print(e)
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
