import logging

from rest_framework import (
    decorators,
    response,
    status,
    viewsets,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.api.v1.api_docs import get_drf_spectacular_view_decorator
from apps.user_app import dtos as user_app_dtos
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

    @decorators.action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAdminUser],
        serializer_class=user_app_serializers.ListUsersSerializer,
    )
    def get_list_of_users(self, request, *args, **kwargs):
        """Вывести пользователей по фильтрам"""
        query_params_serializer = user_app_serializers.UserQueryParamsSerializers(
            data=request.query_params,
        )
        query_params_serializer.is_valid(raise_exception=True)

        query_params = user_app_dtos.UserQueryParamsDTO(
            **query_params_serializer.validated_data,
        )
        users = user_app_services.UserService.get_list_of_users(query_params=query_params)

        filtered_users = self.filter_queryset(users)

        paginator = self.pagination_class()
        paginator.limit = query_params.limit
        paginator.offset = query_params.offset
        page = self.paginate_queryset(filtered_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_users, many=True)

        return response.Response(serializer.data)

    @decorators.action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAdminUser],
        serializer_class=user_app_serializers.UserByIdSerializer,
    )
    def get_user_by_id(self, request, *args, **kwargs):
        """Вывести пользователя по его ID"""
        user_id = kwargs.get("pk")
        user_dto = user_app_services.UserService.get_user_by_id(user_id)

        serializer = self.get_serializer(user_dto)

        return response.Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
