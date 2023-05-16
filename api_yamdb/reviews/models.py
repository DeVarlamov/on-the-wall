from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import MAX_NAME_LENGTH, TRUNCATE_LENGTH
from users.models import User


class Category(models.Model):
    """Категории (типы) произведений"""

    name = models.CharField('имя категории', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('слаг категории', unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return (
            self.name[:TRUNCATE_LENGTH] + '...'
            if len(self.name) > TRUNCATE_LENGTH
            else self.name
        )


class Genre(models.Model):
    """Жанры произведений"""

    name = models.CharField('имя жанра', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField('cлаг жанра', unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return (
            self.name[:TRUNCATE_LENGTH] + '...'
            if len(self.name) > TRUNCATE_LENGTH
            else self.name
        )


class Title(models.Model):
    """Произведения"""

    name = models.CharField(
        'название',
        max_length=MAX_NAME_LENGTH,
        db_index=True,
    )
    year = models.SmallIntegerField(
        'год',
        validators=(
            MaxValueValidator(
                limit_value=datetime.now().year,
                message='год выпуска не может превышать текущий год',
            ),
        ),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True,
    )
    description = models.TextField(
        'описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('name',)

    def __str__(self):
        return (
            self.name[:TRUNCATE_LENGTH] + '...'
            if len(self.name) > TRUNCATE_LENGTH
            else self.name
        )


class Review(models.Model):
    """Отзывы"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
    )
    text = models.CharField('текст', max_length=5000)
    score = models.IntegerField(
        'оценка',
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        error_messages={'validators': 'Оценка только от 1 до 10'},
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                # Ограничение: один отзыв на одно произведение
                fields=(
                    'title',
                    'author',
                ),
                name='unique review',
            ),
        ]

    def __str__(self):
        return (
            self.text[:TRUNCATE_LENGTH] + '...'
            if len(self.text) > TRUNCATE_LENGTH
            else self.text
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
    )
    text = models.CharField('текст комментария', max_length=2000)
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return (
            self.text[:TRUNCATE_LENGTH] + '...'
            if len(self.text) > TRUNCATE_LENGTH
            else self.text
        )
