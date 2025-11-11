from permissions.models import Permission


class PermissionManager:
    '''Отвечает за проверку прав доступа.'''
    def __init__(self, user):
        self.user = user
        self.roles = []
        if user and user.is_authenticated:
            self.roles = user.roles.all()

    def permission_exists(self, resource_type: str, action: str) -> bool:
        '''
        Проверяет, есть ли у пользователя хотя бы одна роль
        с разрешением (resource_type, action).
        '''
        if not self.roles:
            return False
        return Permission.objects.filter(
            role__in=self.roles,
            resource_type__name=resource_type,
            action__name=action,
        ).exists()  # если в БД есть нужный permission, доступ разрешается
