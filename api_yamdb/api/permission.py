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
            request.user.is_admin or request.user.is_superuser)


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
