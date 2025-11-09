from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields) -> None:
        if not email:
            raise ValidationError('Email is required.')
        if not first_name:
            raise ValidationError('First name is required.')
        if not last_name:
            raise ValidationError('Last name is required.')
        
        email = self.normalize_email(email)
        if self.filter(email=email).exists():
            raise ValidationError('User with this email already exists.')
        
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuer must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuer must have is_superuser=True.')
        
        return self.create_user(email, first_name, last_name, password, **extra_fields)
        
