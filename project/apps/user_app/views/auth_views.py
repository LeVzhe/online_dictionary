import logging

from rest_framework import (
    decorators,
    response,
    status,
    viewsets,
)
from rest_framework.permissions import AllowAny

from apps.api.v1.api_docs import get_drf_spectacular_view_decorator
from apps.user_app import serializers as user_app_serializers
from apps.user_app import services as user_app_services

logger = logging.getLogger(__name__)


@get_drf_spectacular_view_decorator("user_app")
class AuthViewset(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["register_user"]:
            return user_app_serializers.RegistrationSerializer
        return super().get_serializer_class()

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
