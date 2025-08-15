import logging

from apps.user_app import repositories as user_app_repositories
from utils.exceptions import BadRequest

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def get_list_of_users(query_params):
        try:
            return user_app_repositories.UserRepository.get_list_of_users_by_filters(query_params)
        except Exception as err:
            logger.exception("Ошибка при обработке данных пользователей.")
            raise BadRequest(detail="Ошибка при обработке данных пользователей.") from err

    @staticmethod
    def get_current_user(current_user):
        return user_app_repositories.UserRepository.get_current_user(current_user=current_user)
