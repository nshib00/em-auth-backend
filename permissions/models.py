from django.db import models

from users.models.roles import Role


class ResourceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'resource_types'


class Action(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'actions'


class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.PROTECT)
    action = models.ForeignKey(Action, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'permissions'
        unique_together = ['role', 'resource_type', 'action']
    
    def __str__(self):
        return f'{self.role.name}_{self.resource_type.name}_{self.action.name}'
