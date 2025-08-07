from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_app.models import User

__all__ = ["CustomUserAdmin"]


class CustomUserAdmin(UserAdmin):
    # Определяем поля, которые будут отображаться в списке пользователей
    list_display = ("username", "email", "first_name", "last_name", "is_staff")

    # Определяем поля для поиска
    search_fields = ("username", "email", "first_name", "last_name")

    # Определяем фильтры
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    # Определяем поля для отображения и редактирования
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Определяем поля, которые будут использоваться при добавлении нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


# Регистрируем модель User с использованием CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
