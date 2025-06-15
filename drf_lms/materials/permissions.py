from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    """
    Разрешение для участников группы 'Moderators'
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Moderators').exists()

class IsOwner(BasePermission):
    """
    Разрешение для владельца объекта
    """
    def has_object_permission(self, request, view, obj):
        return request.user and obj.owner == request.user