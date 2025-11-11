from django.core.management.base import BaseCommand
from django.db import transaction

from permissions.models import Role, Action, ResourceType, Permission
from users.models import User


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Start clearing test data...')

        self.clear_permissions()
        self.clear_roles()
        self.clear_actions()
        self.clear_resource_types()
        self.clear_users()

        self.stdout.write('Test data successfully cleared.')


    def clear_permissions(self):
        '''Очистка всех тестовых прав доступа.'''
        Permission.objects.all().delete()
        self.stdout.write('Deleted test permissions.')

    def clear_roles(self):
        '''Очистка тестовых ролей (admin, manager, user).'''
        roles_to_delete = Role.objects.filter(name__in=['admin', 'manager', 'user'])
        roles_to_delete.delete()
        self.stdout.write('Deleted test roles.')

    def clear_actions(self):
        '''Очистка тестовых действий (view, create, change, delete).'''
        actions_to_delete = Action.objects.filter(name__in=['view', 'create', 'change', 'delete'])
        actions_to_delete.delete()
        self.stdout.write('Deleted test actions.')

    def clear_resource_types(self):
        '''Очистка тестовых типов ресурсов (orders, products).'''
        resources_to_delete = ResourceType.objects.filter(name__in=['orders', 'products'])
        resources_to_delete.delete()
        self.stdout.write('Deleted test resource types.')

    def clear_users(self):
        '''Очистка тестовых пользователей (admin@admin.com, manager@manager.com, user@user.com).'''
        test_users = ['admin@admin.com', 'manager@manager.com', 'user@user.com']
        users_to_delete = User.objects.filter(email__in=test_users)
        users_to_delete.delete()
        self.stdout.write('Deleted test users.')
