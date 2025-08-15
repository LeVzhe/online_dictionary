from rest_framework import serializers

from apps.user_app import models as user_app_models


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        help_text="Личный номер пользователя",
        read_only=True,
    )
    login = serializers.CharField(
        help_text="Login пользователя",
        max_length=user_app_models.User._meta.get_field("username").max_length,
        read_only=True,
    )
    email = serializers.EmailField(
        help_text="Email пользователя",
        max_length=user_app_models.User._meta.get_field("email").max_length,
        read_only=True,
    )
    created_at = serializers.DateTimeField(
        help_text="Дата регистрации пользователя",
        read_only=True,
    )
