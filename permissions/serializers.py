from rest_framework import serializers
from permissions.models import Permission, ResourceType, Action
from users.models.roles import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'is_admin']

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ['id', 'name', 'description']

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'name', 'description']


class PermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )

    resource_type = ResourceTypeSerializer(read_only=True)
    resource_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ResourceType.objects.all(), source='resource_type', write_only=True
    )

    action = ActionSerializer(read_only=True)
    action_id = serializers.PrimaryKeyRelatedField(
        queryset=Action.objects.all(), source='action', write_only=True
    )

    class Meta:
        model = Permission
        fields = [
            'id',
            'role', 'role_id',
            'resource_type', 'resource_type_id',
            'action', 'action_id'
        ]
