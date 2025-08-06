from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from utils import BaseDataModel, UserManager


class User(AbstractUser, BaseDataModel):
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="custom_user_set",  # Уникальное имя для обратной связи
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_permissions_set",  # Уникальное имя для обратной связи
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        indexes = (
            models.Index(
                fields=("-created_at", "-id"),
                name="ix_user_cr_id",
            ),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("email",),
                name="uq_user_email",
                condition=~models.Q(email=""),
            ),
        )
        ordering = (
            "-created_at",
            "-pk",
        )

    REQUIRED_FIELDS = ["email"]

    objects = UserManager()
