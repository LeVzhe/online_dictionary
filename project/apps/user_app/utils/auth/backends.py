from abc import ABC
from typing import NamedTuple

import jwt
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from apps.user_app import models as user_app_models
from apps.user_app.models.session import Session

HTTP_HEADER_ENCODING = "iso-8859-1"


class UserAuth(NamedTuple):
    user: user_app_models.User
    session: Session

    def __str__(self):
        return f"{self.user}, {self.session}"


class JWTBaseAuthentication(BaseAuthentication, ABC):
    def get_token(self, request):
        raise NotImplementedError(_("Реализуйте данный метод в своем подклассе"))

    def authenticate(self, request):
        return self.authenticate_credentials(token=self.get_token(request=request))

    @staticmethod
    def authenticate_credentials(token):
        if not token:
            return None, None

        if isinstance(token, bytes):
            token = token.decode("utf-8")

        secret = getattr(settings, "JWT_SECRET", None)
        if secret is None:
            raise ImproperlyConfigured("settings.JWT_SECRET не сконфигурирован.")

        try:
            decoded_token = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            raise NotAuthenticated(_("Не удалось корректно декодировать токен пользователя")) from None

        try:
            session = Session.objects.select_related("user").get(
                unique_key=decoded_token.get("unique_key"), is_active=True
            )
            return session.user, session
        except Session.DoesNotExist:
            raise NotAuthenticated(_("Пользователь не найден или сессия истекла")) from None


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth_header = request.META.get("HTTP_AUTHORIZATION", b"")
    if isinstance(auth_header, str):
        # Work around django test client oddness
        return auth_header.encode(HTTP_HEADER_ENCODING)

    auth_query = request.query_params.get("token", b"")
    if isinstance(auth_query, str):
        # Work around django test client oddness
        return auth_query.encode(HTTP_HEADER_ENCODING)

    return b""


class JWTHeaderAuthentication(JWTBaseAuthentication):
    www_authenticate_realm = "JWT"

    def get_token(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b"bearer":
            return None

        if len(auth) == 1:
            raise AuthenticationFailed(_("Некорректный заголовок. Учетные данные не были предоставлены"))
        if len(auth) > 2:
            raise AuthenticationFailed(
                _("Некорректный заголовок. Учетные данные не должны содержать пробелов")
            )

        return auth[1]


class JWTHeaderAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "apps.user_app.utils.auth.backends.JWTHeaderAuthentication"
    name = "JWTHeaderAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT authentication via Authorization header",
        }
