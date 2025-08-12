from rest_framework import serializers

from apps.user_app import models as user_app_models


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

    def validate_login(self, value):  # ?! вынести в сервисы
        if user_app_models.User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value

    def validate_email(self, value):  # ?! вынести в сервисы
        if user_app_models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким емейлом уже существует.")
        return value

    def validate(self, data):  # ?! вынести в сервисы
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Поля паролей должны совпадать."})
        return data
