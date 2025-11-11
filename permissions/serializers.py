from rest_framework import serializers
from permissions.models import Permission, ResourceType, Action
from users.models.roles import Role


class PermissionSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(
        source='role.name',
        required=False
    )
    resource_type_name = serializers.CharField(
        source='resource_type.name',
        required=False
    )
    resource_type_description = serializers.CharField(
        source='resource_type.description',
        required=False,
        allow_blank=True
    )
    action_type_name = serializers.CharField(
        source='action.name',
        required=False
    )
    action_type_description = serializers.CharField(
        source='action.description',
        required=False,
        allow_blank=True
    )

    class Meta:
        model = Permission
        fields = [
            'id',
            'role_name',
            'resource_type_name',
            'resource_type_description',
            'action_type_name',
            'action_type_description'
        ]

    def create(self, validated_data):
        role_data = validated_data.pop('role', {})
        resource_data = validated_data.pop('resource_type', {})
        action_data = validated_data.pop('action', {})

        role, _ = Role.objects.get_or_create(
            name=role_data.get('name', 'default_role')
        )

        resource, _ = ResourceType.objects.get_or_create(
            name=resource_data.get('name', 'default_resource'),
            defaults={'description': resource_data.get('description', '')}
        )

        action, _ = Action.objects.get_or_create(
            name=action_data.get('name', 'default_action'),
            defaults={'description': action_data.get('description', '')}
        )

        permission = Permission.objects.create(
            role=role,
            resource_type=resource,
            action=action
        )
        return permission

    def update(self, instance, validated_data):
        role_data = validated_data.pop('role', None)
        if role_data:
            if 'name' in role_data and role_data['name']:
                instance.role, _ = Role.objects.get_or_create(name=role_data['name'])

        resource_data = validated_data.pop('resource_type', None)
        if resource_data:
            if 'name' in resource_data and resource_data['name']:
                instance.resource_type, _ = ResourceType.objects.get_or_create(
                    name=resource_data['name'],
                    defaults={'description': resource_data.get('description', '')}
                )
            if 'description' in resource_data:
                instance.resource_type.description = resource_data['description']
                instance.resource_type.save()

        action_data = validated_data.pop('action', None)
        if action_data:
            if 'name' in action_data and action_data['name']:
                instance.action, _ = Action.objects.get_or_create(
                    name=action_data['name'],
                    defaults={'description': action_data.get('description', '')}
                )
            if 'description' in action_data:
                instance.action.description = action_data['description']
                instance.action.save()

        instance.save()
        return instance
