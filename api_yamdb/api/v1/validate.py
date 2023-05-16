import re

from rest_framework import serializers


def validate_username_me(value):
    """Валидации запрета имя пользователя МЕ"""
    if value.lower() == 'me':
        raise serializers.ValidationError('Имя пользователя `me` недопустимо')
    return value


def validate_username_bad_sign(value):
    """Валидация запрета недопустимых символов"""
    if not re.match(r'^[\w.@+-]+$', value):
        raise serializers.ValidationError(
            'Имя пользователя содержит' 'недопустимые символы',
        )
    return value
