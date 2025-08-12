from http import HTTPStatus

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from apps.user_app import serializers as user_app_serializers

auth_tags = ["auth"]


USER_APP_DECORATORS = {
    "AuthViewset": extend_schema_view(
        register_user=extend_schema(
            tags=auth_tags,
            summary="Зарегистрировать пользователя.",
            request=user_app_serializers.RegistrationSerializer,
            responses={
                HTTPStatus.ACCEPTED: user_app_serializers.UserSerializer,
            },
        )
    ),
}
