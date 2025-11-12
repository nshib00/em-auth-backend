from django.core.management.base import BaseCommand
from django.db import transaction

from permissions.models import Role, Action, ResourceType, Permission
from users.models import User


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Start creating test data...')

        self.create_roles()
        self.create_actions()
        self.create_resource_types()
        self.create_permissions()
        self.create_users()

        self.stdout.write('Test data successfully created.')

    def create_roles(self):
        '''Создание тестовых ролей.'''
        self.admin_role, created = Role.objects.get_or_create(
            name='admin',
            description='Администратор',
            defaults={'is_admin': True}
        )
        if not created:
            if self.admin_role.is_admin is not True:
                self.admin_role.is_admin = True
                self.admin_role.save()

        self.manager_role, _ = Role.objects.get_or_create(
            name='manager',
            description='Менеджер'
        )

        self.user_role, created = Role.objects.get_or_create(
            name='user',
            description='Обычный пользователь',
            defaults={'is_default': True}
        )
        if not created:
            if self.user_role.is_default is not True:
                self.user_role.is_default = True
                self.user_role.save()

        self.stdout.write('Roles created.')

    def create_actions(self):
        '''Создание тестовых пользователей каждой роли.'''
        self.action_view, _ = Action.objects.get_or_create(name='view')
        self.action_create, _ = Action.objects.get_or_create(name='create')
        self.action_change, _ = Action.objects.get_or_create(name='change')
        self.action_delete, _ = Action.objects.get_or_create(name='delete')

        self.stdout.write('Actions created.')

    def create_resource_types(self):
        '''Создание тестовых типов объектов (сами объекты создаются через view).'''
        self.res_orders, _ = ResourceType.objects.get_or_create(name='orders')
        self.res_products, _ = ResourceType.objects.get_or_create(name='products')
        self.stdout.write('Resource types created.')

    def create_permissions(self):
        '''
        Создание разных прав доступа для orders и products:
        - admin: полный доступ к обоим
        - manager: orders (view, change), products (view)
        - user: orders (view), products (нет доступа)
        '''
        roles_to_actions = {
            self.admin_role: {
                self.res_orders: [self.action_view, self.action_create, self.action_change, self.action_delete],
                self.res_products: [self.action_view, self.action_create, self.action_change, self.action_delete],
            },
            self.manager_role: {
                self.res_orders: [self.action_view, self.action_change],
                self.res_products: [self.action_view],
            },
            self.user_role: {
                self.res_orders: [self.action_view],
                self.res_products: [],
            },
        }

        for role, resources in roles_to_actions.items():
            for resource, actions in resources.items():
                for action in actions:
                    Permission.objects.get_or_create(
                        role=role,
                        resource_type=resource,
                        action=action,
                    )

        self.stdout.write('Permissions created.')

    def create_users(self):
        '''Создание тестовых пользователей каждой роли.'''
        admin, created = User.objects.get_or_create(email='admin@admin.com')
        if created:
            admin.set_password('admin123')
            admin.save()
        if not admin.roles.filter(id=self.admin_role.pk).exists():
            admin.roles.add(self.admin_role)

        manager, created = User.objects.get_or_create(email='manager@manager.com')
        if created:
            manager.set_password('manager123')
            manager.save()
        if not manager.roles.filter(id=self.manager_role.pk).exists():
            manager.roles.add(self.manager_role)

        user, created = User.objects.get_or_create(email='user@user.com')
        if created:
            user.set_password('user123')
            user.save()
        if not user.roles.filter(id=self.user_role.pk).exists():
            user.roles.add(self.user_role)

        self.stdout.write('Users created.')
