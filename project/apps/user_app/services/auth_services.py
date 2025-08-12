import logging

from apps.user_app import repositories as user_app_repositories
from utils import exceptions

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def register_user(data):
        try:
            return user_app_repositories.AuthRepository.create_register_user(data=data)
        except Exception as err:
            logger.exception("Ошибка при обработке данных пользователя.")
            raise exceptions.BadRequest(detail="Ошибка при обработке данных пользователя.") from err
