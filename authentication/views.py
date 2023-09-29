from rest_framework import views, permissions, status, generics
from rest_framework.response import Response

from django.contrib.auth.models import User

from . import serializers


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer
