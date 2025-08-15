import logging

from rest_framework import (
    decorators,
    response,
    status,
    viewsets,
)
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.api_docs import get_drf_spectacular_view_decorator
from apps.user_app import serializers as user_app_serializers
from apps.user_app import services as user_app_services

logger = logging.getLogger(__name__)


__all__ = [
    "UserViewset",
]


@get_drf_spectacular_view_decorator("user_app")
class UserViewset(viewsets.GenericViewSet):
    @decorators.action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        serializer_class=user_app_serializers.CurrentUserSerializer,
    )
    def get_current_user(self, request):
        """Вывести текущего пользователя"""
        current_user = request.user
        user_dto = user_app_services.UserService.get_current_user(current_user=current_user)
        serializer = self.get_serializer(user_dto)
        return response.Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
