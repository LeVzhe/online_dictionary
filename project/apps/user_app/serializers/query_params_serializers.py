from rest_framework import serializers


class UserQueryParamsSerializers(serializers.Serializer):
    limit = serializers.IntegerField(
        help_text="Количество возвращаемых результатов на страницу",
        required=False,
    )
    offset = serializers.IntegerField(
        help_text="Инициализация индекса, по которому возвращаются результаты",
        required=False,
    )

    is_archived = serializers.BooleanField(
        help_text="Пользователь активен?",
        required=False,
        allow_null=True,
    )
