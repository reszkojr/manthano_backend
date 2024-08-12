from django.contrib.auth import authenticate
from authentication.models import *
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=ManthanoUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': "Password fields do not match."})
        return data

    def create(self, validated_data):
        user = ManthanoUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = ManthanoUser
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username,' 'email', 'first_name', 'last_name')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['enrollment']

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['academic_rank', 'subjects']

class ClassroomUserSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True, source='user_professor')
    student = StudentSerializer(read_only=True, source='user_student')
    role = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username', 'student', 'professor', 'role')

    def get_role(self, instance):
        if instance.is_student():
            return 'student'
        if instance.is_professor():
            return 'professor'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['profile_picture'] = instance.profile.profile_picture or None
        ret['profile_background'] = instance.profile.profile_background or None
        return ret


