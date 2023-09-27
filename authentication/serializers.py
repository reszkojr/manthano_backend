from django.contrib.auth import authenticate

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True,
    )
    password = serializers.CharField(
        label="Password",
        write_only=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        print(self.context.get('request'))
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = 'Both "username" and "password" are required.'
                raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
