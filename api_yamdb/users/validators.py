import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Валидация запрета недопустимых символов
    """
    invalid_chars_regex = re.compile(r'[^\w.@+-]+')
    invalid_chars = re.findall(invalid_chars_regex, value)

    if invalid_chars:
        raise ValidationError(
            'Имя пользователя содержит недопустимые'
            f'символы: {", ".join(invalid_chars)}',
        )

    if value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя не может быть "me".',
        )

    return value
