from django_filters import CharFilter, FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр по полям тайтла."""

    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')
