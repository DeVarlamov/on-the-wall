from django.forms import ValidationError
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для пользовательской модели."""

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
        validators=(validate_username,),
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def create(self, validated_data):
        """Метод создает новый пользовательский объект"""
        user_by_username = User.objects.filter(
            username=validated_data.get('username'),
        ).first()
        user_by_email = User.objects.filter(
            email=validated_data.get('email'),
        ).first()
        if not any((user_by_username, user_by_email)):
            return User.objects.create(**validated_data)
        elif user_by_email == user_by_username:
            return user_by_username
        raise ValidationError('User или Email уже заняты')

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
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        model = Title

    def to_representation(self, instance):
        return TitleGetSerializer(instance).data


class TitleGetSerializer(serializers.ModelSerializer):
    """Класс сериализатора для запросов на получение тайтлов."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True, default=0)

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
        if self.context.get('request').method != 'POST':
            return data
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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(  # type: ignore [var-annotated]
        slug_field='username',
        read_only=True,
    )

    class Meta:
        exclude = ['review']
        model = Comment
