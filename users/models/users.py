from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from users.models.roles import Role, UserRole
from users.managers import UserManager
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, default='')
    date_joined = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, default=None)
    roles = models.ManyToManyField(Role, through=UserRole)
    
    # поля для django admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()


    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        if self.middle_name:
            full_name = f'{self.last_name} {self.first_name} {self.middle_name}'
        return full_name.strip()
    
    def get_short_name(self):
        return self.first_name
    
    # реализация мягкого удаления пользователя
    def delete(self):
        self.is_active = False
        self.date_deleted = timezone.now()
        self.save()