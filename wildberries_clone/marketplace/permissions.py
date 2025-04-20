from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ на чтение для всех пользователей,
    а на запись - только аутентифицированным.
    """
    def has_permission(self, request, view):
        # Разрешить GET, HEAD, OPTIONS запросы всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить запись только аутентифицированным пользователям
        return request.user and request.user.is_authenticated