import re

from rest_framework import serializers


def validate_username(value):
    """
    Валидация запрета недопустимых символов
    """
    if not re.match(r'^(?!me$|ME$)[\w.@+-]+\Z', value):
        raise serializers.ValidationError(
            f'Имя пользователя содержит {value}',
        )
    return value
