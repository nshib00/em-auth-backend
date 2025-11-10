from django.db import models
from django.contrib.auth import get_user_model



class RefreshToken(models.Model):
    jti = models.CharField(max_length=36, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )


class BlacklistedToken(models.Model):
    jti = models.CharField(max_length=36, unique=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    expires_at = models.DateTimeField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)
