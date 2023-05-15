from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.v1.validate import validate_username_bad_sign, validate_username_me
from reviews.models import Category, Genre, Title, User, Comment, Review


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для пользовательской модели."""

    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username_bad_sign,
            UniqueValidator(queryset=User.objects.all()),
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    """Класс сериализатора для редактирования
    объектов пользовательской модели
    """

    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username_bad_sign,
        ],
    )
    email = serializers.EmailField(
        max_length=254,
    )
    role = serializers.CharField(
        max_length=20,
        read_only=True,
    )
    bio = serializers.CharField()
    first_name = serializers.CharField(
        max_length=150,
    )
    last_name = serializers.CharField(
        max_length=150,
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    """Класс сериализатора для регистрации новых пользователей."""

    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username_me,
            validate_username_bad_sign,
        ],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def create(self, validated_data):
        """Метод создает новый пользовательский объект"""
        try:
            user = User.objects.get_or_create(**validated_data)[0]
        except IntegrityError:
            raise ValidationError('User или Email уже заняты')
        return user

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    """Класс сериализатора для генерации и проверки токенов аутентификации."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """Класс сериализатора для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Класс сериализатора для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitlePostSerializer(serializers.ModelSerializer):
    """Класс сериализатора для запросов на создание тайтлов."""

    category = serializers.SlugRelatedField(  # type: ignore [var-annotated]
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(  # type: ignore [var-annotated]
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    """Класс сериализатора для запросов на получение тайтлов."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(  # type: ignore [var-annotated]
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        """Предотвращает повторные отзывы от одного пользователя"""
        if (
            self.context.get('request').method == 'POST'
            and Review.objects.filter(
                author=self.context.get('request').user,
                title=self.context.get('view').kwargs.get('title_id'),
            ).exists()
        ):
            raise serializers.ValidationError(
                'Ваш отзыв уже имеется',
            )
        return data

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка только от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(  # type: ignore [var-annotated]
        slug_field='text',
        read_only=True,
    )
    author = serializers.SlugRelatedField(  # type: ignore [var-annotated]
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment


'''
class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
'''
