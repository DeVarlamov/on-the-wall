from api import serializers
from api.permissions import IsAdminUserOrReadOnly
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from reviews.models import Category, Genre, Title


class CreateRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class GenreViewSet(CreateRetrieveViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateRetrieveViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'category__slug', 'genre__slug', 'year')
