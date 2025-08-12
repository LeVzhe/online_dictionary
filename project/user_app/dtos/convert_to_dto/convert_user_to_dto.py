import logging

from django.core.exceptions import ValidationError

from user_app import dtos as user_app_dtos

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
