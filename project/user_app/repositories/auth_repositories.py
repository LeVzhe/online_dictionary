from user_app import models as user_app_models
from user_app.dtos.convert_to_dto import convert_registered_user_to_dto


class AuthRepository:
    @staticmethod
    def create_register_user(data):
        user = user_app_models.User.objects.create_user(
            username=data["login"],
            email=data["email"],
            password=data["password"],
        )
        user.save()

        return convert_registered_user_to_dto(row=user)
