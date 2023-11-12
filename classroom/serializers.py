from rest_framework import serializers

from .models import *


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = instance.user.username
        ret['avatar'] = 'instance.user.profile.profile_picture'
        return ret
