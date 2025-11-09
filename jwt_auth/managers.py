
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import AuthenticationFailed

from jwt_auth.models import RefreshToken
from jwt_auth.token_data import TokenPair, TokenType


class JWTTokenManager:
    @classmethod
    def _get_active_user(cls, user_id: int) -> AbstractBaseUser:
        '''Вспомогательная функция для получения активного пользователя'''
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise AuthenticationFailed('User account is disabled')
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

    @classmethod
    def _get_token_payload(cls, token: str, verify_exp: bool = True) -> dict:
        '''Декодирование токена'''
        return jwt.decode(
            jwt=token,
            key=settings.TOKEN_SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM],
            options={'verify_exp': verify_exp}
        )

    @classmethod
    def create_token(cls, user_id: int, token_type: TokenType) -> str:
        '''Создание access/refresh токена'''
        time_now = datetime.now(timezone.utc)
        payload = {
            'sub': str(user_id),
            'iat': time_now,
            'jti': str(uuid4()),
            'type': token_type.value,
        }
        if token_type == TokenType.ACCESS:
            payload |= {
                'exp': time_now + timedelta(minutes=15)
            }
        elif token_type == TokenType.REFRESH:
            payload |= {
                'exp': time_now + timedelta(days=30)
            }
        token = jwt.encode(
            payload,
            key=settings.TOKEN_SECRET_KEY,
            algorithm=settings.TOKEN_ALGORITHM
        )
        return token
    
    @classmethod
    def save_refresh_token(cls, refresh_token: str, user_id: int) -> None:
        '''Сохранение refresh токена в БД'''
        payload = cls._get_token_payload(refresh_token)
        RefreshToken.objects.create(
            token=refresh_token,
            user_id=user_id,
            expires_at=datetime.fromtimestamp(payload['exp'], tz=timezone.utc),
        )
    
    @classmethod
    def create_token_pair(cls, user_id: int) -> TokenPair:
        '''Создание пары токенов access-refresh с сохранением refresh токена в БД'''
        access_token = cls.create_token(user_id, TokenType.ACCESS)
        refresh_token = cls.create_token(user_id, TokenType.REFRESH)
        cls.save_refresh_token(refresh_token, user_id)
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    
    @classmethod
    def authenticate_by_access_token(cls, token: str) -> AbstractBaseUser:
        '''Аутентификация по access токену'''
        if not settings.TOKEN_SECRET_KEY or not settings.TOKEN_ALGORITHM:
            raise AuthenticationFailed('JWT config error')
        try:
            payload = cls._get_token_payload(token)
            if payload.get('type') != TokenType.ACCESS.value:
                raise AuthenticationFailed('Invalid token type')
            user_id = payload.get('sub')
            if user_id is None:
                raise AuthenticationFailed('Token does not contain user_id')
            
            return cls._get_active_user(int(user_id))

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token is expired')
        except jwt.PyJWTError:
            raise AuthenticationFailed('Invalid token')
        except (ValueError, TypeError):
            raise AuthenticationFailed('Invalid user_id in token')
        except AuthenticationFailed:
            raise
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')
        
    @classmethod
    def verify_refresh_token(cls, refresh_token: str) -> bool:
        '''Проверка валидности refresh токена'''
        try:
            payload = cls._get_token_payload(refresh_token)
            
            if payload.get('type') != TokenType.REFRESH.value:
                return False
            
            return RefreshToken.objects.filter(
                token=refresh_token,
                expires_at__gt=datetime.now(timezone.utc)
            ).exists()
        except jwt.PyJWTError:
            return False
        
    @classmethod
    def refresh_token_pair(cls, refresh_token: str) -> TokenPair:
        '''Получение по refresh токену новой пары токенов (access + refresh)'''
        if not cls.verify_refresh_token(refresh_token):
            raise AuthenticationFailed('Invalid or expired refresh token')
        
        payload = cls._get_token_payload(refresh_token)
        user_id = int(payload['sub'])
        old_refresh_jti = payload['jti']

        new_token_pair = cls.create_token_pair(user_id)
        RefreshToken.objects.filter(jti=old_refresh_jti).delete()

        return new_token_pair

    @classmethod
    def delete_user_refresh_tokens(cls, user_id: int) -> None:
        '''Удаление всех токенов пользователя (для logout и деактивации)'''
        RefreshToken.objects.filter(user_id=user_id).delete()

