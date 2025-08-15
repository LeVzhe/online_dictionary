from apps.user_app.dtos.convert_to_dto import convert_row_to_user_dto


class UserRepository:
    @staticmethod
    def get_current_user(current_user):
        return convert_row_to_user_dto(current_user)
