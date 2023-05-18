from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from api.v1.permissions import IsAdminUserOrReadOnly


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Набор представлений, который предоставляет действия
    `create()`, `list()` и `destroy()`.
    Методы:
    - `create(request, *args, **kwargs)`: Создайте новый экземпляр модели.
    - `list(request, *args, **kwargs)`: Возвращает список всех существующих
    экземпляров модели.
    - `уничтожить(запрос, *args, **kwargs)`: Удалить экземпляр модели.
    """

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']
