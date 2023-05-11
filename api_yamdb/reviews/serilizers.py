from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
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
