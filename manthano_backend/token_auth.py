from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.db import close_old_connections

from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken

from jwt import InvalidTokenError
from jwt import decode as jwt_decode

from urllib.parse import parse_qs, urlparse

from manthano_backend import settings


@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        return user

    except get_user_model().DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        close_old_connections()

        # Get the token
        qs = parse_qs(dict(scope)['query_string'])
        if b'token' not in qs.keys():
            return await send({
                "type": "websocket.close",
                "code": 403
            })
        token = qs[b'token'][0]

        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return None

        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = await get_user(validated_token=decoded_data)

        if not user.is_authenticated:
            return await send({
                "type": "websocket.close",
                "code": 403
            })
        scope["user"] = user
        return await super().__call__(scope, receive, send)

        return await super().__call__(scope, receive, send)
