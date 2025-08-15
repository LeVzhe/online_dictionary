import logging
import typing
from http import HTTPStatus

from rest_framework import (
    decorators,
    response,
    status,
    viewsets,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.api.v1.api_docs import get_drf_spectacular_view_decorator
from apps.user_app import dtos as user_app_dtos
from apps.user_app import serializers as user_app_serializers
from apps.user_app import services as user_app_services
from apps.user_app.models.session import Session
from utils.user_agent import get_user_agent

logger = logging.getLogger(__name__)

__all__ = [
    "AuthViewset",
]


@get_drf_spectacular_view_decorator("user_app")
class AuthViewset(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["register_user"]:
            return user_app_serializers.RegistrationSerializer
        return user_app_serializers.LoginUsingUsernamePassword

    @decorators.action(
        detail=False,
        methods=["POST"],
    )
    def register_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        register_data_dto = user_app_services.AuthService.register_user(data=validated_data)
        user_serializer = user_app_serializers.UserSerializer(register_data_dto)

        logger.info(f"Пользователь {user_serializer.data['login']} был зарегистрирован.")
        return response.Response(
            data=user_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(
        detail=False,
        methods=["POST"],
    )
    def login_using_username_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_agent = get_user_agent(request=request)
        dto = user_app_dtos.LoginUsingUsernamePasswordDto(
            **serializer.validated_data,
            user_agent=user_agent,
        )
        session = user_app_services.AuthService.login_using_username_password(dto=dto)
        serialized_data = user_app_serializers.LoginResultSerializer(instance=session).data
        return response.Response(data=serialized_data, status=HTTPStatus.CREATED)

    @decorators.action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        typing.cast(Session, request.auth).logout()
        return response.Response(data=user_app_serializers.GenericResponseSerializer(instance={}).data)
