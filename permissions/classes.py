from rest_framework.permissions import BasePermission
from permissions.managers import PermissionManager
from users.models.roles import Role


class ResourceActionPermission(BasePermission):
    '''
    Проверяет, есть ли у пользователя с ролями (roles)
    разрешение на выполнение действия (action) над ресурсом (resource_type). 
    '''
    def has_permission(self, request, view) -> bool:
        permission_manager = PermissionManager(request.user)

        # если resource_type и action переданы во view как атрибуты класса,
        # то они подтягиваются автоматически 
        resource_type = getattr(view, 'resource_type', None)
        action = getattr(view, 'action', None)

        if resource_type is None or action is None:
            return False

        return permission_manager.permission_exists(resource_type, action)
    

class IsAdmin(BasePermission):
    '''
    Проверяет, является ли пользователь администратором.
    '''
    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.roles.filter(is_admin=True).exists()
