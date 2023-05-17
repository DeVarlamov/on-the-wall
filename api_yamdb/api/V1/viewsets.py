from rest_framework import mixins, viewsets


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

    pass
