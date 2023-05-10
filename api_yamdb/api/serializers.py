from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(  # type: ignore [var-annotated]
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True,
    )

    genre = serializers.SlugRelatedField(  # type: ignore [var-annotated]
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True,
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
