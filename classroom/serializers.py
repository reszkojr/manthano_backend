from rest_framework import serializers, validators

from authentication.serializers import ClassroomUserSerializer, UserSerializer

from .models import *

class ClassroomSerializer(serializers.ModelSerializer):
    channels = serializers.SerializerMethodField()
    jitsi_channels = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = '__all__'

    def get_channels(self, instance):
        if hasattr(instance, 'channels'):
            return ChannelSerializer(instance.channels, many=True).data
        return []

    def get_jitsi_channels(self, instance):
        if hasattr(instance, 'jitsi_channels'):
            return JitsiChannelSerializer(instance.jitsi_channels, many=True).data
        return []

    def get_users(self, instance):
        if hasattr(instance, 'users'):
            return ClassroomUserSerializer(instance.users, many=True).data
        return []


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class JitsiChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JitsiChannel
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

        validators = [
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'date', 'text'),
            )
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user_id'] = instance.user.id
        ret['username'] = instance.user.username
        ret['avatar'] = 'https://static.vecteezy.com/system/resources/previews/024/983/914/non_2x/simple-user-default-icon-free-png.png'
        return ret
