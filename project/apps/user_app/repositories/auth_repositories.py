from rest_framework.serializers import ValidationError

from apps.user_app import models as user_app_models
from apps.user_app.dtos.convert_to_dto import convert_registered_user_to_dto


class AuthRepository:
    @staticmethod
    def create_register_user(data):
        if user_app_models.User.objects.filter(username=data["login"]).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        if user_app_models.User.objects.filter(email=data["email"]).exists():
            raise ValidationError("Пользователь с таким емейлом уже существует.")

        user = user_app_models.User.objects.create_user(
            username=data["login"],
            email=data["email"],
            password=data["password"],
        )
        user.save()

        return convert_registered_user_to_dto(row=user)

    @staticmethod
    def login_using_username_password(username):
        user = user_app_models.User.objects.get(username=username)
        return user
