from rest_framework import serializers


class AppResponseStatusField(serializers.ChoiceField):
    """
    Стандартное поле для передачи статуса операции
    """

    def __init__(self, choices: list[str] | None = None, **kwargs):
        choices = choices or ["ok"]
        defaule_value = kwargs.get("default") or choices[0]
        default_kwargs: dict = {
            "read_only": True,
            "default": defaule_value,
        }
        super().__init__(choices, **(default_kwargs | kwargs))
