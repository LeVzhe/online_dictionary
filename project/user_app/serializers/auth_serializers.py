from rest_framework import serializers

from user_app import models as user_app_models


class RegistrationSerializer(serializers.Serializer):
    password = serializers.CharField(
        help_text="Пароль",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("password").max_length,
    )
    login = serializers.CharField(
        help_text="Login пользователя",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("username").max_length,
    )
    email = serializers.EmailField(
        help_text="Email пользователя",
        min_length=1,
        max_length=user_app_models.User._meta.get_field("email").max_length,
    )

    def validate_login(self, value):  # ?! вынести в сервисы
        if user_app_models.User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value

    def validate_email(self, value):  # ?! вынести в сервисы
        if user_app_models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким емейлом уже существует.")
        return value
