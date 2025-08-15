import logging

from django.core.exceptions import ValidationError

from apps.user_app import dtos as user_app_dtos

logger = logging.getLogger(__name__)


def convert_registered_user_to_dto(row):
    try:
        res = user_app_dtos.UserDTO.model_validate(
            {
                "login": row.username,
                "email": row.email,
            },
            from_attributes=True,
        )
        return res
    except ValidationError as err:
        logger.error(f"Ошибка валидации при преобразовании RegisteredUser в UserDTO: {err}")
        raise ValidationError("Ошибка валидации данных:") from err


def convert_row_to_user_dto(row):
    try:
        res = user_app_dtos.CurrentUserDTO.model_validate(
            {
                "id": row.id,
                "login": row.username,
                "email": row.email,
                "created_at": row.created_at,
            },
            from_attributes=True,
        )
        return res
    except ValidationError as err:
        logger.error(f"Ошибка валидации при преобразовании RegisteredUser в UserDTO: {err}")
        raise ValidationError("Ошибка валидации данных:") from err
