from django.contrib import admin


class AppBaseAdmin(admin.ModelAdmin):
    """
    Базовый класс для моделей в интерфейсе администратора
    """

    save_on_top = True

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not obj:
            fields = tuple(item for item in fields if item not in self.readonly_fields)
        return fields
