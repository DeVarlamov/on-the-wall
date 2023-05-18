from django.contrib.auth.models import AbstractUser
from django.db import models

from api.v1.validate import validate_username
from api_yamdb.settings import ADMIN, MODERATOR, USER

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        db_index=True,
        validators=(validate_username,),
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
