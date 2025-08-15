from apps.user_app import repositories as user_app_repositories


class UserService:
    @staticmethod
    def get_current_user(current_user):
        return user_app_repositories.UserRepository.get_current_user(current_user=current_user)
