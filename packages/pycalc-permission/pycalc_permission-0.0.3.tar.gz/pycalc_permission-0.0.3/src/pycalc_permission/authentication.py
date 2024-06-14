from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .token import decode_token
from .user import JwtUser
# from django.contrib.auth.models import User


class JWTAuthentication(BaseAuthentication):
    """
            custom authentication class for DRF and JWT
    """

    keyword = 'Auth'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    @staticmethod
    def authenticate_credentials(token):
        user = decode_token(token)
        return JwtUser(user), None

    def authenticate_header(self, request):
        return self.keyword
