
from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import AuthenticationFailed


class JWTTokenManager:
    def _get_active_user(self, user_id: int) -> AbstractBaseUser:
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise AuthenticationFailed('User account is disabled')
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')


    def create_access_token(self, user_id: int) -> str:
        time_now = datetime.now(timezone.utc)
        payload = {
            'sub': str(user_id),
            'iat': time_now,
            'exp': time_now + timedelta(minutes=15),
            'type': 'access',
        }
        token = jwt.encode(
            payload,
            key=settings.TOKEN_SECRET_KEY,
            algorithm=settings.TOKEN_ALGORITHM
        )
        return token


    def authenticate_by_access_token(self, token: str) -> AbstractBaseUser:
        if not settings.TOKEN_SECRET_KEY or not settings.TOKEN_ALGORITHM:
            raise AuthenticationFailed('JWT config error')
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.TOKEN_SECRET_KEY,
                algorithms=[settings.TOKEN_ALGORITHM],
                options={'verify_exp': True}
            )
            
            if payload.get('type') != 'access':
                raise AuthenticationFailed('Invalid token type')
            
            user_id: str = payload.get('sub')
            if not user_id:
                raise AuthenticationFailed('Token does not contain user_id')
            
            return self._get_active_user(int(user_id))

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
