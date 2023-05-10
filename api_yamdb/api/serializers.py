from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.validate import validate_username_me, validate_username_bad_sign

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для пользовательской модели."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username_bad_sign,
            UniqueValidator(queryset=User.objects.all()
                            )
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    """Класс сериализатора для редактирования
        объектов пользовательской модели
    """
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    """Класс сериализатора для регистрации новых пользователей."""
    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username_me,
            validate_username_bad_sign,
        ]
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def create(self, validated_data):
        """Метод создает новый пользовательский объект"""
        try:
            user = User.objects.get_or_create(**validated_data)[0]
        except IntegrityError:
            raise ValidationError("User или Email уже заняты")
        return user

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    """Класс сериализатора для генерации и проверки токенов аутентификации."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
