import re

from django.core.exceptions import ValidationError


def validate_username_me(value):
    """Валидации запрета имя пользователя МЕ"""
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя `me` недопустимо')
    return value


def validate_username_bad_sign(value):
    """Валидация запрета недопустимых символов"""
    legals = re.compile(r'^[\w.@+-]+\Z')
    if not re.match(legals, value):
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы: '
            f'{" ".join([char for char in value if not legals.match(char)])}',
        )
    return value
