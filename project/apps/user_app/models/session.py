import datetime
import uuid

import jwt
from django.conf import settings
from django.db import models
from django.utils import timezone

from utils.base_model import BaseDjangoModel

__all__ = [
    "Session",
]


class Session(
    BaseDjangoModel,
):
    """
    Сессия пользователя
    """

    class Meta:
        verbose_name = "Сессия пользователя"
        verbose_name_plural = "Сессии пользователей"
        indexes = (
            models.Index(
                fields=(
                    "-created_at",
                    "-id",
                ),
                name="ix_user_session_cr_id",
            ),
        )
        ordering = (
            "-created_at",
            "-pk",
        )

    user = models.ForeignKey(
        to="user_app.User",
        related_name="sessions",
        verbose_name="Владелец сессии",
        on_delete=models.CASCADE,
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Представление агента сессии",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Сессия активна",
    )
    unique_key = models.CharField(
        unique=True,
        max_length=36,
        verbose_name="Уникальный код",
    )

    @property
    def token(self):
        return self._generate_jwt_token()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.unique_key = str(uuid.uuid4())
        return super().save(*args, **kwargs)

    def _generate_jwt_token(self):
        expiry_date = timezone.now() + datetime.timedelta(days=90)

        return jwt.encode(
            {
                "id": self.pk,
                "exp": int(expiry_date.timestamp()),
                "unique_key": self.unique_key,
            },
            settings.JWT_SECRET,
            algorithm="HS256",
        )

    def logout(self):
        """
        Завершить сессию
        """
        return self.delete()
