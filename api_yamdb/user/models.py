from django.contrib.auth.models import AbstractUser

from django.db import models

from api.V1.validate import validate_username


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """Модель пользователя.

    Её необходимо переопределить, что бы добавить
    поля с биографией, ролью и т.д.
    """

    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
        verbose_name='email пользоаптеля'
    )
    role = models.CharField(
        verbose_name='роль',
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='о себе любимом',
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
