from django.utils.translation import gettext_lazy as _
from rest_framework import fields, serializers

from apps.user_app import models as user_app_models
from apps.user_app.utils.serializers.fields import AppResponseStatusField


class UserSerializer(serializers.Serializer):
    login = serializers.CharField(
        help_text="Login пользователя",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("username").max_length,
        default="",
    )
    email = serializers.EmailField(
        help_text="Email пользователя",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("email").max_length,
        default="",
    )


class RegistrationSerializer(serializers.Serializer):
    login = serializers.CharField(
        required=True,
        help_text="Login пользователя",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("username").max_length,
    )
    email = serializers.EmailField(
        required=True,
        help_text="Email пользователя",
        min_length=5,
        max_length=user_app_models.User._meta.get_field("email").max_length,
        style={"type": "email"},
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Пароль",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("password").max_length,
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Проверка пароля",
        min_length=1,
        style={"input_type": "password"},
    )


class LoginUsingUsernamePassword(serializers.Serializer):
    login = serializers.CharField(
        required=True,
        help_text="Login пользователя",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("username").max_length,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Пароль",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("password").max_length,
        style={"input_type": "password"},
    )


class LoginResultUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_null=True)


class LoginResultSerializer(serializers.Serializer):
    token = fields.CharField(help_text=_("JWT токен сессии"))
    user = LoginResultUserSerializer(help_text=_("Пользователь"))


class GenericResponseSerializer(serializers.Serializer):
    status = AppResponseStatusField()
