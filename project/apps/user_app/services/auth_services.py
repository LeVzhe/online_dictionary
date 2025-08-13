import logging

from django.core import exceptions as django_exceptions
from django.utils.translation import gettext_lazy as _

from apps.user_app import models as user_app_models
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

    @staticmethod
    def login_using_username_password(dto):
        """
        Создать и вернуть сессию по 'username' и паролю
        """
        err = django_exceptions.ValidationError(
            message=_("Пользователь не найден."),
        )
        try:
            user = user_app_models.User.objects.get(username=dto.login)  # !!! перенести в репозиторий
        except user_app_models.User.DoesNotExist:
            raise err from None
        if not user.check_password(dto.password):
            raise err
        return user.create_session(user_agent=dto.user_agent)
