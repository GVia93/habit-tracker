from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request


class IsOwnerOrReadOnly(BasePermission):
    """Разрешает изменение объекта только владельцу, чтение — всем (в рамках queryset)."""

    def has_object_permission(self, request: Request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "user_id", None) == getattr(request.user, "id", None)
