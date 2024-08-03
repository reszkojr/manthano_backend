from rest_framework import serializers, validators

from authentication.serializers import ClassroomUserSerializer

from .models import *


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if hasattr(instance, 'channels'):
            ret['channels'] = ChannelSerializer(instance.channels, many=True).data
        else:
            ret['channels'] = []

        if hasattr(instance, 'jitsi_channels'):
            ret['jitsi_channels'] = JitsiChannelSerializer(instance.jitsi_channels, many=True).data
        else:
            ret['jitsi_channels'] = []

        if hasattr(instance, 'users'):
            ret['users'] = ClassroomUserSerializer(instance.users, many=True).data
        else:
            ret['users'] = []

        return ret


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
