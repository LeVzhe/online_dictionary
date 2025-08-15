from django.db.models import Q

from apps.user_app import models as user_app_models
from apps.user_app.dtos.convert_to_dto import (
    convert_row_to_user_dto,
    convert_row_to_user_list_dto,
)


class UserRepository:
    @staticmethod
    def _build_filters(query_params):
        filters = Q()

        if query_params.is_archived is True:
            filters &= ~Q(is_archived=True)
        elif query_params.is_archived is False:
            filters &= Q(is_archived=True)

        return filters

    @staticmethod
    def get_list_of_users_by_filters(query_params):
        filters = UserRepository._build_filters(query_params=query_params)
        users = user_app_models.User.objects.filter(filters).order_by("-created_at")

        return [convert_row_to_user_list_dto(row) for row in users]

    @staticmethod
    def get_current_user(current_user):
        return convert_row_to_user_dto(current_user)
