from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'is_superuser', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Личная информация', {'fields': ['first_name', 'last_name', 'middle_name']}),
        ('Права доступа и роли', {
            'fields': ['is_active', 'is_staff', 'is_superuser'],
        }),
        ('Даты', {'fields': ['last_login', 'date_joined', 'date_deleted']}),
    ]
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'first_name', 'last_name', 'password1', 'password2'],
        }),
    ]
    readonly_fields = ['last_login', 'date_joined', 'date_deleted']


admin.site.register(User, UserAdmin)