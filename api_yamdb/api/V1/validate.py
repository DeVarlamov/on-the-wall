import re

from rest_framework import serializers


def validate_username(value):
    """
    Валидация запрета недопустимых символов
    """
    invalid_chars = re.findall(r'[^\w.@+-]+', value)
    if invalid_chars:
        invalid_chars_str = ', '.join(invalid_chars)
        raise serializers.ValidationError(
            'Имя пользователя содержит запрещенные'
            f'символы: {invalid_chars_str}',
        )
    return value
