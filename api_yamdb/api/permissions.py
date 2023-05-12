from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Пользовательский класс разрешений, который проверяет, является ли
    запрашивающий пользователь администратором.
    Этот класс разрешений разрешает доступ только прошедшим проверку
    подлинности пользователям, имеющим административные привилегии,
    а именно, что они являются либо администратором, либо суперпользователем.
    Атрибуты:
    Никто.
    Методы:
    has_permission(self, request, view): проверяет, есть ли у запрашивающего
    пользователя разрешение на запрашиваемое действие.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminUserOrReadOnly(IsAdmin):
    """
    Пользовательский класс разрешений, который проверяет, является ли
    запрашивающий пользователь администратором.
    Этот класс позволяет выполнять запросы на изменение информации
    только пользователям с правами администратора. Все прочие
    пользователи могут выполнять запросы только на чтение информации.
    Атрибуты:
    Никто.
    Методы:
    has_permission(self, request, view): проверяет, есть ли у запрашивающего
    пользователя разрешение на запрашиваемое действие.
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin



class IsAdminModeratorAuthorPermission(permissions.BasePermission):

    message = 'Запрос доступен только администратору, модератору или владельцу.'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
