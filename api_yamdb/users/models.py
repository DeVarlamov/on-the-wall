from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


def validate_username_not_equal_me(value):
    if value != 'me':
        return value
    else:
        raise ValidationError('`me` не может использоваться в качестве имени')


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        db_index=True,
        validators=(
            UnicodeUsernameValidator(),
            validate_username_not_equal_me,
        ),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        'роль',
        max_length=100,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
