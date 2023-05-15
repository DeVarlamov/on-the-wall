from django_filters import AllValuesFilter, CharFilter, FilterSet, NumberFilter

from reviews.models import Title

""" class TitleFilter(FilterSet):

    category = AllValuesFilter(field_name='category__slug')
    genre = AllValuesFilter(field_name='genre__slug')
    year = NumberFilter(field_name='year')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year') """


from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр по полям тайтла."""

    # category = CharFilter(field_name='category__slug')
    # genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre__slug', 'category__slug')
